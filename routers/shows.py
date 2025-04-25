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
from datetime import datetime

router = APIRouter()


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
