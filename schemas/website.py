from pydantic import BaseModel, field_validator
from typing import Optional, ClassVar, Set


class WebsiteBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    icon: Optional[str] = None


class WebsiteCreate(WebsiteBase):
    _existing_urls: ClassVar[Set[str]] = set()

    @field_validator("url")
    @classmethod
    def url_must_be_unique(cls, v):
        if v in cls._existing_urls:
            raise ValueError("URL already exists")
        return v

    @classmethod
    def set_existing_urls(cls, urls):
        cls._existing_urls = set(urls)


class WebsiteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None

    _existing_urls: ClassVar[Set[str]] = set()

    @field_validator("url")
    @classmethod
    def url_must_be_unique_on_update(cls, v):
        if v is not None and v in cls._existing_urls:
            raise ValueError("URL already exists")
        return v

    @classmethod
    def set_existing_urls(cls, urls):
        cls._existing_urls = set(urls)


class Website(WebsiteBase):
    id: int

    class Config:
        from_attributes = True
