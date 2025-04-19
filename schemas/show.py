from pydantic import BaseModel


class ShowBase(BaseModel):
    title: str
    description: str


class ShowCreate(ShowBase):
    pass


class ShowUpdate(BaseModel):
    pass


class Show(ShowBase):
    id: int

    class Config:
        from_attributes = True
