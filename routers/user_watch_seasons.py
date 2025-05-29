# filepath: c:\\Users\\user\\Desktop\\Codes\\MovieBrowser2_backend\\routers\\user_watch_seasons.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.user_watch_season import UserWatchSeason as UserWatchSeasonModel
from schemas.user_watch_season import UserWatchSeason as UserWatchSeasonSchema
from middleware.authenticated_route import authenticated_route


router = APIRouter()


@router.get("/", response_model=List[UserWatchSeasonSchema])
@authenticated_route
async def get_user_watch_seasons(
    request: Request, show_id: Optional[int] = None, season_id: Optional[int] = None, db: Session = Depends(get_db)
):
    user = request.state.user
    query = db.query(UserWatchSeasonModel).filter(UserWatchSeasonModel.user_id == user.id)

    if show_id is not None:
        query = query.filter(UserWatchSeasonModel.show_id == show_id)

    if season_id is not None:
        query = query.filter(UserWatchSeasonModel.season_id == season_id)

    user_watch_seasons = query.all()
    return user_watch_seasons
