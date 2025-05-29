from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from middleware.authenticated_route import authenticated_route
from middleware.is_admin import is_admin
from schemas.website import Website, WebsiteCreate, WebsiteUpdate
from models.website import Website as WebsiteModel
from database import get_db
from seeders.website_seeder import WebsiteSeeder
from sqlalchemy import or_
from models.website_tag import WebsiteTag  # Added import

router = APIRouter()


@router.get("/", response_model=List[Website])
def read_websites(
    request: Request,
    db: Session = Depends(get_db),
    tags: Optional[str] = None,
    description: Optional[str] = None,
    title: Optional[str] = None,
):
    query = db.query(WebsiteModel)

    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]

        # Build an OR query so that any tag match is sufficient

        tag_filters = [WebsiteTag.name.ilike(f"%{tag}%") for tag in tag_list]
        if tag_filters:
            query = query.join(WebsiteModel.tags).filter(or_(*tag_filters))

    if description:
        query = query.filter(WebsiteModel.description.ilike(f"%{description}%"))

    if title:
        query = query.filter(WebsiteModel.title.ilike(f"%{title}%"))

    websites = query.all()
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

    website = WebsiteModel(
        title=data.title,
        description=data.description,
        url=data.url,
        icon=data.icon,
    )
    db.add(website)
    db.flush()  # get website.id for tags

    if data.tags:
        website.sync_tags(data.tags, db)

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
    tags = update_data.pop("tags", None)

    for k, v in update_data.items():
        setattr(website, k, v)

    if tags is not None:
        website.sync_tags(tags, db)

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


@router.post("/seed")
@authenticated_route
@is_admin
def seed_websites_route(request: Request, db: Session = Depends(get_db)):
    """
    Seed/update websites from the default JSON file.
    """
    WebsiteSeeder(db).seed()
    return {"ok": True, "message": "Websites seeded from default_websites.json"}
