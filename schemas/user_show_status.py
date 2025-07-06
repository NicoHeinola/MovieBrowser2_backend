from pydantic import BaseModel
from typing import Optional


class UserShowStatus(BaseModel):
    id: Optional[int] = None
    show_id: int
    status: str

    class Config:
        orm_mode = True
