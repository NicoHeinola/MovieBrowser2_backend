from sqlalchemy import Column, Integer, String
from models.base import Base


class TorrentWebsite(Base):
    __tablename__ = "torrent_websites"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    url = Column(String, unique=True, nullable=False, index=True)
    icon = Column(String, nullable=True)
