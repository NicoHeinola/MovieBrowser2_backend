from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base


class UserShowStatus(Base):
    __tablename__ = "user_show_statuses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User")
    show = relationship("Show")
