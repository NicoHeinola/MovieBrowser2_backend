from sqlalchemy import Column, Integer, String
from models.base import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)
