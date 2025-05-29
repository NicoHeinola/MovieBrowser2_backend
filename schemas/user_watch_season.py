from pydantic import BaseModel
from typing import Optional, List
from .episode import Episode  # Import Episode from new file


class UserWatchSeason(BaseModel):
    id: Optional[int] = None
    season_id: int
