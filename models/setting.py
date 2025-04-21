from sqlalchemy import Column, Integer, String
from models.base import Base


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'int', 'string', 'float', 'boolean'
