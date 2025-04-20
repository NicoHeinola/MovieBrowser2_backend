from pydantic import BaseModel
from typing import Optional


class ShowBase(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None


class ShowCreate(ShowBase):
    pass


class ShowUpdate(ShowBase):
    pass


class Show(ShowBase):
    id: int

    class Config:
        from_attributes = True
