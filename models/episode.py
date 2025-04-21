from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    number = Column(Integer, nullable=False)
    type = Column(String, nullable=True)  # New column added
    season = relationship("Season", back_populates="episodes")
