from pydantic import BaseModel
from typing import Optional, List
from .season import Season  # Import Season from new file


class ShowBase(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    seasons: List[Season] = []


class ShowCreate(ShowBase):
    pass


class ShowUpdate(ShowBase):
    pass


class Show(ShowBase):
    folder_name: str  # New field

    class Config:
        from_attributes = True
