import os
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from models.setting import Setting
from schemas.episode import Episode
from schemas.show import Show, ShowCreate, ShowUpdate
from models.show import Show as ShowModel
from database import get_db
from models.episode import Episode as EpisodeModel
from models.season import Season as SeasonModel
from models.show import Show as ShowModel
from utils.vlc_media_player_util import VLCMediaPlayerUtil

router = APIRouter()


@router.get("/", response_model=List[Show])
def read_shows(request: Request, db: Session = Depends(get_db)):
    query_params = request.query_params

    query = db.query(ShowModel)

    if "search[search]" in query_params:
        query = ShowModel.filterBySearch(query, query_params.get("search[search]"))

    shows = query.all()

    return shows


@router.get("/{show_id}", response_model=Show)
def read_show(show_id: int, db: Session = Depends(get_db)):
    show = db.query(ShowModel).filter(ShowModel.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show


@router.post("/", response_model=Show)
def create_show(data: ShowCreate, db: Session = Depends(get_db)):
    db_show = ShowModel(
        description=data.description,
        image=data.image,
    )

    db_show.set_title(data.title)

    db.add(db_show)
    db.flush()

    if data.seasons is not None:
        seasons = [season.model_dump() for season in data.seasons]
        db_show.sync_seasons(seasons, db)

    db.commit()
    db.refresh(db_show)
    return db_show


@router.put("/{show_id}", response_model=Show)
def update_show(show_id: int, data: ShowUpdate, db: Session = Depends(get_db)):
    db_show = db.query(ShowModel).filter(ShowModel.id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=404, detail="Show not found")

    update_data = data.model_dump(exclude={"seasons", "title"})

    for key, value in update_data.items():
        setattr(db_show, key, value)

    # If title is updated, update folder_name (contains the show's episodes)
    if data.title:
        db_show.set_title(data.title)

    if data.seasons is not None:
        seasons = [season.model_dump() for season in data.seasons]
        db_show.sync_seasons(seasons, db)

    db.commit()
    db.refresh(db_show)
    return db_show


@router.delete("/{show_id}")
def delete_show(show_id: int, db: Session = Depends(get_db)):
    show = db.query(ShowModel).filter(ShowModel.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    show.delete_folder()
    db.delete(show)
    db.commit()
    return {"ok": True}


@router.post("/{show_id}/episodes/{episode_id}/file", response_model=Episode)
def upload_episode_file(show_id: int, episode_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    episode = db.query(EpisodeModel).filter(EpisodeModel.id == episode_id).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    # Attach file to episode model
    episode.attach_file(file)

    db.commit()
    db.refresh(episode)

    return episode


# Removes unused files and folders that may not have been removed due to errors
@router.post("/cleanup")
def upload_episode_file(db: Session = Depends(get_db)):
    shows = db.query(ShowModel).filter().all()

    files_to_keep: list = []
    for show in shows:
        for season in show.seasons:
            for episode in season.episodes:
                episode_file_path: str = episode.get_full_file_path()
                if not episode_file_path:
                    continue

                if os.path.exists(episode_file_path):
                    files_to_keep.append(episode_file_path)

        show_folder = show.get_full_folder_path()
        if not os.path.exists(show_folder):
            continue

    base_folder: str = Setting.get_shows_folder_path()

    if not base_folder:
        raise HTTPException(status_code=500, detail="Base folder for shows is not configured.")

    removable_file_types: list = ["mkv", "mp4", "mov", "avi", "webm"]

    for root, dirs, files in os.walk(base_folder):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1][1:].lower()
            if file_path not in files_to_keep and ext in removable_file_types:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

    # Remove empty folders (including those that only contain empty folders)
    for dirpath, dirnames, filenames in os.walk(base_folder, topdown=False):
        try:
            # If all contents are directories and all are empty, remove them recursively
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
        except Exception as e:
            print(f"Failed to remove folder {dirpath}: {e}")

    return {}


@router.post("/{show_id}/episodes/{episode_id}/watch")
def watch_episode(show_id: int, episode_id: int, db: Session = Depends(get_db)):  # Changed parameters
    # Fetch the episode using the ID
    episode = (
        db.query(EpisodeModel).filter(EpisodeModel.id == episode_id, EpisodeModel.season.has(show_id=show_id)).first()
    )

    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found for this show")

    file_path: str = episode.get_full_file_path()
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Episode file not found")

    try:
        VLCMediaPlayerUtil.open_file(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="VLC media player not found on this system.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open file with VLC: {e}")

    return {"ok": True}


@router.post("/{show_id}/seasons/{season_id}/watch")
def watch_season(
    show_id: int, season_id: int, db: Session = Depends(get_db)
):  # Changed parameters and function name for clarity
    # Fetch the season using the ID
    season = db.query(SeasonModel).filter(SeasonModel.id == season_id, SeasonModel.show_id == show_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found for this show")

    folder_path: str = season.get_full_folder_path()
    if not folder_path or not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="Season folder not found")

    try:
        VLCMediaPlayerUtil.open_playlist_from_folder(folder_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="VLC media player not found on this system.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open playlist with VLC: {e}")

    return {"ok": True}
