from pydantic import BaseModel
from typing import Optional, List
from .episode import Episode  # Import Episode from new file


class Season(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    number: int
    episodes: List[Episode] = []
