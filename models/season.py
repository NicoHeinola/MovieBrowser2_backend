import datetime
import os
import shutil
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from models.base import Base
from models.episode import Episode


class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    number = Column(Integer, nullable=False)
    folder_name = Column(String, nullable=False)
    show = relationship("Show", back_populates="seasons")
    episodes = relationship("Episode", back_populates="season", cascade="all, delete-orphan")

    @staticmethod
    def create_unique_folder_safe_name(season_number: int) -> str:
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"season_{season_number}_{date_str}"

    def get_full_folder_path(self) -> str | None:
        if not self.folder_name:
            return None

        show_folder_path: str = self.show.get_full_folder_path()

        if not show_folder_path:
            return None

        full_path: str = os.path.join(show_folder_path, self.folder_name)

        full_path = full_path.replace("\\", "/")

        return full_path

    def sync_episodes(self, episodes_data, db: Session):
        episode_ids_to_delete = set()
        for episode in self.episodes:
            episode_ids_to_delete.add(episode.id)

        for episode in episodes_data:
            id = episode.get("id")
            episode_model: Episode = db.query(Episode).filter(Episode.id == id).first()

            blacklisted_keys = ["number", "title", "file_size"]
            filtered_episode_data = {k: v for k, v in episode.items() if k not in blacklisted_keys}

            if episode_model:
                for key, value in filtered_episode_data.items():
                    setattr(episode_model, key, value)
            else:
                episode_model = Episode(**filtered_episode_data)
                episode_model.season = self
                self.episodes.append(episode_model)

            # Always set number and title using their setters
            if "number" in episode:
                episode_model.set_number(episode["number"])
            if "title" in episode:
                episode_model.set_title(episode["title"])

            episode_model.update_file_size_bytes()

            db.add(episode_model)

            # Sync episodes
            db.flush()

            # Do not delete the updated/created episode
            if episode_model.id in episode_ids_to_delete:
                episode_ids_to_delete.remove(episode_model.id)

        # Remove episodes that are not in the new data
        for episode_id in episode_ids_to_delete:
            episode_to_delete = db.query(Episode).filter(Episode.id == episode_id).first()
            if not episode_to_delete:
                continue

            episode_to_delete.delete_file()
            db.delete(episode_to_delete)

        db.commit()

    def set_number(self, new_number: int):
        if new_number == self.number:
            return

        # Update the episode number in the database
        self.number = new_number
        self.rename_folder()

    def rename_folder(self):
        """
        Rename the seasons' folder on disk.
        """
        old_folder_path: str | None = self.get_full_folder_path()

        self.folder_name = self.create_unique_folder_safe_name(self.number)

        new_folder_path: str | None = self.get_full_folder_path()

        if old_folder_path and os.path.exists(old_folder_path):
            os.rename(old_folder_path, new_folder_path)

    def delete_folder(self):
        """
        Delete the seasons' folder on disk.
        """

        full_folder_path: str = self.get_full_folder_path()
        if full_folder_path and os.path.exists(full_folder_path):
            shutil.rmtree(full_folder_path)
