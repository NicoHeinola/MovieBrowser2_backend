from pydantic import BaseModel


class WebsiteTag(BaseModel):
    name: str
