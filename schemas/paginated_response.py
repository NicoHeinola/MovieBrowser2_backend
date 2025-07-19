from pydantic import BaseModel
from typing import Any, List


class Pagination(BaseModel):
    total: int
    page: int
    pages: int
    limit: int


class PaginatedResponse(BaseModel):
    data: List[Any]
    pagination: Pagination

    class Config:
        orm_mode = True
