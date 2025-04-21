from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from schemas.show import Show, ShowCreate, ShowUpdate
from models.show import Show as ShowModel
from database import get_db

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
def create_show(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    seasons: Optional[str] = Form(None),
    image: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    db_show = ShowModel(
        title=title,
        description=description,
        image=image,
    )
    db.add(db_show)
    db.flush()

    if seasons:
        try:
            seasons_data = json.loads(seasons)
            db_show.sync_seasons(seasons_data, db)
        except Exception:
            pass

    db.commit()
    db.refresh(db_show)
    return db_show


@router.put("/{show_id}", response_model=Show)
def update_show(
    show_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    seasons: Optional[str] = Form(None),
    image: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    db_show = db.query(ShowModel).filter(ShowModel.id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=404, detail="Show not found")

    db_show.title = title
    db_show.description = description
    db_show.image = image

    if seasons:
        try:
            seasons_data = json.loads(seasons)
            db_show.sync_seasons(seasons_data, db)
        except Exception:
            pass

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
