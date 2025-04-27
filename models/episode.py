import datetime
import re
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

import os

from models.setting import Setting


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

    @staticmethod
    def create_unique_episode_name(episode_number: int) -> str:
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"episode_{episode_number}_{date_str}"

    def get_full_file_path(self) -> str | None:
        # Get the season folder path
        season_folder_path = self.season.get_full_folder_path()
        if not season_folder_path:
            return None

        if not self.filename:
            return None

        # Construct the full file path
        full_file_path = os.path.join(season_folder_path, self.filename)
        return full_file_path

    def set_number(self, new_number: int):
        if new_number == self.number:
            return

        # Update the episode number in the database
        self.number = new_number
        self.rename_file()

    def rename_file(self):
        # Update the filename to reflect the new number
        if not self.filename:
            return

        season_directory = self.season.get_full_folder_path()
        os.makedirs(season_directory, exist_ok=True)

        file_path: str = self.get_full_file_path()
        file_extension = os.path.splitext(file_path)[1]
        unique_filename: str = self.create_unique_episode_name(self.number)
        episode_filename = f"{unique_filename}{file_extension}"
        full_save_path = os.path.join(season_directory, episode_filename)

        if file_path and os.path.exists(file_path):
            os.rename(file_path, full_save_path)

        self.filename = episode_filename

    def attach_file(self, file):
        # Create the SEASON directory if it doesn't exist
        season_directory = self.season.get_full_folder_path()
        os.makedirs(season_directory, exist_ok=True)

        # Figure out stuff
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename: str = self.create_unique_episode_name(self.number)
        episode_filename = f"{unique_filename}{file_extension}"
        full_save_path = os.path.join(season_directory, episode_filename)

        # Write the file to the disk
        with open(full_save_path, "wb+") as output_file:
            output_file.write(file.file.read())

        # Update the filename in the database
        self.filename = episode_filename

        return episode_filename

    def delete_file(self):
        full_file_path: str = self.get_full_file_path()

        if full_file_path and os.path.exists(full_file_path):
            os.remove(full_file_path)
