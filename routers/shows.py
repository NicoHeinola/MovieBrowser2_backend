from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_database
from models import show as show_model
from schemas import show as show_schema

router = APIRouter()


@router.post("/", response_model=show_schema.Show)
def create_show(show: show_schema.ShowCreate, db: Session = Depends(get_database)):
    db_show = show_model.Show(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show


@router.put("/{show_id}", response_model=show_schema.Show)
def update_show(show_id: int, show_update: show_schema.ShowUpdate, db: Session = Depends(get_database)):
    db_show = db.query(show_model.Show).filter(show_model.Show.id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=404, detail="Show not found")
    for key, value in show_update.dict().items():
        setattr(db_show, key, value)
    db.commit()
    db.refresh(db_show)
    return db_show


@router.get("/", response_model=list[show_schema.Show])
def read_shows(skip: int = 0, limit: int = 10, db: Session = Depends(get_database)):
    return db.query(show_model.Show).offset(skip).limit(limit).all()


@router.get("/{show_id}", response_model=show_schema.Show)
def read_show(show_id: int, db: Session = Depends(get_database)):
    show = db.query(show_model.Show).filter(show_model.Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show
