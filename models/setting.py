from sqlalchemy import Column, Integer, String
from database import get_db
from models.base import Base


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'int', 'string', 'float', 'boolean'

    @staticmethod
    def get_shows_folder_path() -> str | None:
        db = next(get_db())
        setting = db.query(Setting).filter(Setting.key == "shows_path").first()

        if not setting:
            return None

        return setting.value
