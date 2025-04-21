from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import re

from schemas.episode import Episode
from schemas.show import Show, ShowCreate, ShowUpdate
from models.show import Show as ShowModel
from models.setting import Setting as SettingModel
from database import get_db
from models.episode import Episode as EpisodeModel
from models.season import Season as SeasonModel
from models.show import Show as ShowModel

router = APIRouter()


def folder_safe_name(title: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", title).strip("_").lower()


@router.get("/", response_model=List[Show])
def read_shows(db: Session = Depends(get_db)):
    shows = db.query(ShowModel).all()
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
        title=data.title,
        description=data.description,
        image=data.image,
        folder_name=folder_safe_name(data.title),  # Set folder_name
    )

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

    update_data = data.model_dump(exclude={"seasons"})
    old_folder_name = db_show.folder_name

    for key, value in update_data.items():
        setattr(db_show, key, value)

    # If title is updated, update folder_name
    if "title" in update_data and update_data["title"]:
        new_folder_name = folder_safe_name(update_data["title"])
        if new_folder_name != db_show.folder_name:
            db_show.folder_name = new_folder_name

            shows_path_setting = db.query(SettingModel).filter(SettingModel.key == "shows_path").first()
            if not shows_path_setting:
                raise HTTPException(status_code=500, detail="Shows path not configured in settings")

            shows_path = shows_path_setting.value
            db_show.rename_folder(old_folder_name, shows_path)

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
    db.delete(show)
    db.commit()
    return {"ok": True}


@router.post("/shows/{show_id}/episodes/{episode_id}/file", response_model=Episode)
def upload_episode_file(show_id: int, episode_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    episode = db.query(EpisodeModel).filter(EpisodeModel.id == episode_id).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    season = db.query(SeasonModel).filter(SeasonModel.id == episode.season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    show = db.query(ShowModel).filter(ShowModel.id == season.show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    # Load shows_path from settings
    shows_path = db.query(SettingModel).filter(SettingModel.key == "shows_path").first()

    if not shows_path:
        raise HTTPException(status_code=500, detail="Shows path not configured in settings")

    # Use model method to attach file
    episode.attach_file(file, show.title, season.number, shows_path)

    db.commit()
    db.refresh(episode)

    return episode
