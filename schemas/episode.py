from pydantic import BaseModel
from typing import Optional


class Episode(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    number: int
    type: Optional[str] = None
    filename: Optional[str] = None
    file_size_bytes: Optional[int] = None
