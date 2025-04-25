import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import os
import re

from models.base import Base
from models.season import Season
from models.setting import Setting


class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    folder_name = Column(String, nullable=False)
    seasons = relationship("Season", back_populates="show", cascade="all, delete-orphan")

    @staticmethod
    def create_unique_folder_safe_name(title: str) -> str:
        safe_title = re.sub(r"[^a-zA-Z0-9_-]", "_", title).strip("_").lower()
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        return f"{safe_title}_{date_str}"

    def __init__(self, *args, **kwargs):
        if "title" in kwargs and "folder_name" not in kwargs:
            kwargs["folder_name"] = self.create_unique_folder_safe_name(kwargs["title"])
        super().__init__(*args, **kwargs)

    def sync_seasons(self, seasons_data, db: Session):

        season_ids_to_delete = set()
        for season in self.seasons:
            season_ids_to_delete.add(season.id)

        for season in seasons_data:
            id = season.get("id")
            season_model: Season = db.query(Season).filter(Season.id == id).first()

            blacklisted_keys = ["episodes"]

            if season_model:
                for key, value in season.items():
                    if key in blacklisted_keys:
                        continue

                    setattr(season_model, key, value)
                db.add(season_model)
            else:
                season_data = season.copy()
                for key in blacklisted_keys:
                    season_data.pop(key, None)

                season_model = Season(**season_data)
                db.add(season_model)
                self.seasons.append(season_model)

            # Sync episodes
            db.flush()
            if "episodes" in season:
                season_model.sync_episodes(season["episodes"], db)

            # Do not delete the updated/created season
            if season_model.id in season_ids_to_delete:
                season_ids_to_delete.remove(season_model.id)

        # Remove seasons that are not in the new data
        for season_id in season_ids_to_delete:
            season_to_delete = db.query(Season).filter(Season.id == season_id).first()
            if season_to_delete:
                db.delete(season_to_delete)

        db.commit()

    def update_title(self, new_title: str):
        """
        Update the show's title and folder name.
        """

        if self.title == new_title:
            return

        self.title = new_title
        self.rename_folder()

    def rename_folder(self):
        """
        Rename the show's folder on disk if the folder_name changes.
        """
        shows_path: str = Setting.get_shows_folder_path()
        if not shows_path:
            raise Exception("Shows path not configured in settings")

        self.folder_name = self.create_unique_folder_safe_name(self.title)

        # No need to rename anything if we don't have a folder name
        if not self.folder_name:
            return

        old_path: str = os.path.join(shows_path, self.folder_name)
        new_path: str = os.path.join(shows_path, self.folder_name)

        old_path = old_path.replace("\\", "/")
        new_path = new_path.replace("\\", "/")

        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    def delete_folder(self):
        """
        Delete the show's folder on disk.
        """
        shows_path: str = Setting.get_shows_folder_path()
        if not shows_path:
            raise Exception("Shows path not configured in settings")

        path = os.path.join(shows_path, self.folder_name)
        if os.path.exists(path):
            os.rmdir(path)
