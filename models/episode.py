from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

import os


class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    number = Column(Integer, nullable=False)
    type = Column(String, nullable=True)  # New column added
    filename = Column(String, nullable=True)  # New column for file name
    season = relationship("Season", back_populates="episodes")

    def attach_file(self, file, show_title: str, season_number: int, shows_base_path: str):
        file_extension = os.path.splitext(file.filename)[1]
        episode_filename = f"episode_{self.number}{file_extension}"

        show_directory = os.path.join(shows_base_path, show_title)
        season_directory = os.path.join(show_directory, f"season_{season_number}")

        os.makedirs(season_directory, exist_ok=True)

        full_save_path = os.path.join(season_directory, episode_filename)

        with open(full_save_path, "wb+") as output_file:
            output_file.write(file.file.read())

        self.filename = episode_filename

        return episode_filename
