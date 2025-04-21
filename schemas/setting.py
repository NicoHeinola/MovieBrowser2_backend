from pydantic import BaseModel, field_validator
from typing import Optional, ClassVar, Set


class SettingBase(BaseModel):
    key: str
    value: str
    type: str


class SettingCreate(SettingBase):
    _existing_keys: ClassVar[Set[str]] = set()

    @field_validator("key")
    @classmethod
    def key_must_be_unique(cls, v):
        if v in cls._existing_keys:
            raise ValueError("Key already exists")
        return v

    @classmethod
    def set_existing_keys(cls, keys):
        cls._existing_keys = set(keys)


class SettingUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None

    _existing_keys: ClassVar[Set[str]] = set()

    @field_validator("key")
    @classmethod
    def key_must_be_unique_on_update(cls, v):
        if v is not None and v in cls._existing_keys:
            raise ValueError("Key already exists")
        return v

    @classmethod
    def set_existing_keys(cls, keys):
        cls._existing_keys = set(keys)


class Setting(SettingBase):
    id: int

    class Config:
        from_attributes = True
