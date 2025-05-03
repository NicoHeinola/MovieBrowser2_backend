from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from middleware.authenticated_route import authenticated_route
from middleware.is_admin import is_admin
from schemas.website import Website, WebsiteCreate, WebsiteUpdate
from models.website import Website as WebsiteModel
from database import get_db

router = APIRouter()


@router.get("/", response_model=List[Website])
def read_websites(request: Request, db: Session = Depends(get_db)):
    websites = db.query(WebsiteModel).all()
    return websites


@router.get("/{id}", response_model=Website)
def read_website(request: Request, id: int, db: Session = Depends(get_db)):
    website = db.query(WebsiteModel).filter(WebsiteModel.id == id).first()

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    return website


@router.post("/", response_model=Website)
@authenticated_route
@is_admin
def create_website(request: Request, data: WebsiteCreate, db: Session = Depends(get_db)):
    url: str = data.model_dump().get("url")

    if db.query(WebsiteModel).filter(WebsiteModel.url == url).first():
        raise HTTPException(status_code=400, detail="URL already exists")

    website = WebsiteModel(**data.model_dump())
    db.add(website)
    db.commit()
    db.refresh(website)

    return website


@router.put("/{id}", response_model=Website)
@authenticated_route
@is_admin
def update_website(request: Request, id: int, data: WebsiteUpdate, db: Session = Depends(get_db)):
    website = db.query(WebsiteModel).filter(WebsiteModel.id == id).first()

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    update_data = data.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(website, k, v)

    db.commit()
    db.refresh(website)

    return website


@router.delete("/{id}", response_model=Website)
@authenticated_route
@is_admin
def delete_website(request: Request, id: int, db: Session = Depends(get_db)):
    website = db.query(WebsiteModel).filter(WebsiteModel.id == id).first()

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    db.delete(website)
    db.commit()

    return website
