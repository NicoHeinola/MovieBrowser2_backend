import datetime
import re
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
    type = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    file_size_bytes = Column(Integer, nullable=True)

    season = relationship("Season", back_populates="episodes")

    @staticmethod
    def create_unique_episode_name(episode_number: int, title: str | None) -> str:
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        safe_title = "no_title"
        if title:
            safe_title = re.sub(r"[^a-zA-Z]", "_", title).strip("_").lower()

        formatted_number: str = f"{episode_number:03d}"

        return f"ep_{formatted_number}_{safe_title}_date_{date_str}_ep_{formatted_number}"

    def get_full_file_path(self) -> str | None:
        # Get the season folder path
        season_folder_path = self.season.get_full_folder_path()
        if not season_folder_path:
            return None

        if not self.filename:
            return None

        # Construct the full file path
        full_file_path: str = os.path.join(season_folder_path, self.filename)

        full_file_path = full_file_path.replace("\\", "/")

        return full_file_path

    def update_file_size_bytes(self):
        full_file_path: str = self.get_full_file_path()
        if full_file_path and os.path.exists(full_file_path):
            self.file_size_bytes = os.path.getsize(full_file_path)
        else:
            self.file_size_bytes = 0

    def set_title(self, new_title: str):
        if new_title == self.title:
            return

        self.title = new_title
        self.rename_file()

    def set_number(self, new_number: int):
        if new_number == self.number:
            return

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
        unique_filename: str = self.create_unique_episode_name(self.number, self.title)
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
        unique_filename: str = self.create_unique_episode_name(self.number, self.title)
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
