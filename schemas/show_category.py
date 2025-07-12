from pydantic import BaseModel


class ShowCategory(BaseModel):
    name: str
