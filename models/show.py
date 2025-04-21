from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import os
import re

from models.base import Base
from models.season import Season


def folder_safe_name(title: str) -> str:
    # Replace non-alphanumeric characters with underscores and lowercase
    return re.sub(r"[^a-zA-Z0-9_-]", "_", title).strip("_").lower()


class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    folder_name = Column(String, nullable=False)
    seasons = relationship("Season", back_populates="show", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        if "title" in kwargs and "folder_name" not in kwargs:
            kwargs["folder_name"] = folder_safe_name(kwargs["title"])
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

    def rename_folder(self, old_folder_name: str, shows_path: str):
        """
        Rename the show's folder on disk if the folder_name changes.
        """
        old_path = os.path.join(shows_path, old_folder_name)
        new_path = os.path.join(shows_path, self.folder_name)

        old_path = old_path.replace("\\", "/")
        new_path = new_path.replace("\\", "/")

        if old_folder_name != self.folder_name and os.path.exists(old_path):
            os.rename(old_path, new_path)
