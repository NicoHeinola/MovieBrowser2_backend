from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from middleware.authenticated_route import authenticated_route
from middleware.is_admin import is_admin
from schemas.torrent_website import TorrentWebsite, TorrentWebsiteCreate, TorrentWebsiteUpdate
from models.torrent_website import TorrentWebsite as TorrentWebsiteModel
from database import get_db

router = APIRouter()


@router.get("/", response_model=List[TorrentWebsite])
def read_torrent_websites(request: Request, db: Session = Depends(get_db)):
    torrent_websites = db.query(TorrentWebsiteModel).all()
    return torrent_websites


@router.get("/{id}", response_model=TorrentWebsite)
def read_torrent_website(request: Request, id: int, db: Session = Depends(get_db)):
    torrent_website = db.query(TorrentWebsiteModel).filter(TorrentWebsiteModel.id == id).first()

    if not torrent_website:
        raise HTTPException(status_code=404, detail="Torrent website not found")

    return torrent_website


@router.post("/", response_model=TorrentWebsite)
@authenticated_route
@is_admin
def create_torrent_website(request: Request, data: TorrentWebsiteCreate, db: Session = Depends(get_db)):
    url: str = data.model_dump().get("url")

    if db.query(TorrentWebsiteModel).filter(TorrentWebsiteModel.url == url).first():
        raise HTTPException(status_code=400, detail="URL already exists")

    torrent_website = TorrentWebsiteModel(**data.model_dump())
    db.add(torrent_website)
    db.commit()
    db.refresh(torrent_website)

    return torrent_website


@router.put("/{id}", response_model=TorrentWebsite)
@authenticated_route
@is_admin
def update_torrent_website(request: Request, id: int, data: TorrentWebsiteUpdate, db: Session = Depends(get_db)):
    torrent_website = db.query(TorrentWebsiteModel).filter(TorrentWebsiteModel.id == id).first()

    if not torrent_website:
        raise HTTPException(status_code=404, detail="Torrent website not found")

    update_data = data.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(torrent_website, k, v)

    db.commit()
    db.refresh(torrent_website)

    return torrent_website


@router.delete("/{id}", response_model=TorrentWebsite)
@authenticated_route
@is_admin
def delete_torrent_website(request: Request, id: int, db: Session = Depends(get_db)):
    torrent_website = db.query(TorrentWebsiteModel).filter(TorrentWebsiteModel.id == id).first()

    if not torrent_website:
        raise HTTPException(status_code=404, detail="Torrent website not found")

    db.delete(torrent_website)
    db.commit()

    return torrent_website
