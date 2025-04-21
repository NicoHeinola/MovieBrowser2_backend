from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.show import Show, ShowCreate, ShowUpdate
from models.show import Show as ShowModel, Season as SeasonModel, Episode as EpisodeModel
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
def create_show(data: ShowCreate, db: Session = Depends(get_db)):
    db_show = ShowModel(**data.model_dump())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show


@router.put("/{show_id}", response_model=Show)
def update_show(show_id: int, data: ShowUpdate, db: Session = Depends(get_db)):
    db_show = db.query(ShowModel).filter(ShowModel.id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=404, detail="Show not found")

    update_data = data.model_dump()
    for key, value in update_data.items():
        setattr(db_show, key, value)

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
