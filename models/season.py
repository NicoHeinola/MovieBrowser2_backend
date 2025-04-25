import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from models.base import Base
from models.episode import Episode
from models.setting import Setting


class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    number = Column(Integer, nullable=False)
    show = relationship("Show", back_populates="seasons")
    episodes = relationship("Episode", back_populates="season", cascade="all, delete-orphan")

    def sync_episodes(self, episodes_data, db: Session):
        episode_ids_to_delete = set()
        for episode in self.episodes:
            episode_ids_to_delete.add(episode.id)

        for episode in episodes_data:
            id = episode.get("id")
            episode_model: Episode = db.query(Episode).filter(Episode.id == id).first()

            if episode_model:
                blacklisted_keys = ["number"]
                for key, value in episode.items():
                    if key in blacklisted_keys:
                        continue

                    setattr(episode_model, key, value)

                if "number" in episode:
                    episode_model.update_number(episode["number"])

                db.add(episode_model)
            else:
                episode_model = Episode(**episode)
                self.episodes.append(episode_model)
                db.add(episode_model)

            # Sync episodes
            db.flush()

            # Do not delete the updated/created episode
            if episode_model.id in episode_ids_to_delete:
                episode_ids_to_delete.remove(episode_model.id)

        # Remove episodes that are not in the new data
        for episode_id in episode_ids_to_delete:
            episode_to_delete = db.query(Episode).filter(Episode.id == episode_id).first()
            if episode_to_delete:
                db.delete(episode_to_delete)

        db.commit()

    def get_full_folder_path(self) -> str:
        shows_folder_path = Setting.get_shows_folder_path()
        return os.path.join(shows_folder_path, self.show.folder_name, f"season_{self.number}")
