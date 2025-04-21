from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from models.base import Base
from models.season import Season


class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    seasons = relationship("Season", back_populates="show", cascade="all, delete-orphan")

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
