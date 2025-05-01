from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.setting import Setting, SettingCreate, SettingUpdate
from models.setting import Setting as SettingModel
from database import get_db
from seeders.setting_seeder import SettingSeeder

router = APIRouter()


@router.get("/", response_model=List[Setting])
def read_settings(db: Session = Depends(get_db)):
    settings = db.query(SettingModel).all()
    return settings


@router.get("/{id}", response_model=Setting)
def read_setting(id: str, db: Session = Depends(get_db)):
    setting = db.query(SettingModel).filter(SettingModel.id == id).first()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    return setting


@router.post("/", response_model=Setting)
def create_setting(data: SettingCreate, db: Session = Depends(get_db)):
    key: str = data.model_dump().get("key")

    if db.query(SettingModel).filter(SettingModel.key == key).first():
        raise HTTPException(status_code=400, detail="Key already exists")

    setting = SettingModel(**data.model_dump())
    db.add(setting)
    db.commit()
    db.refresh(setting)

    return setting


@router.put("/{id}", response_model=Setting)
def update_setting(id: str, data: SettingUpdate, db: Session = Depends(get_db)):
    setting = db.query(SettingModel).filter(SettingModel.id == id).first()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    update_data = data.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(setting, k, v)

    db.commit()
    db.refresh(setting)

    return setting


@router.delete("/{id}", response_model=Setting)
def delete_setting(id: str, db: Session = Depends(get_db)):
    setting = db.query(SettingModel).filter(SettingModel.id == id).first()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    db.delete(setting)
    db.commit()

    return setting


@router.post("/seed")
def seed_settings_route(db: Session = Depends(get_db)):
    """
    Seed/update settings from the default JSON file.
    """
    SettingSeeder(db).seed()
    return {"ok": True, "message": "Settings seeded from default_settings.json"}
