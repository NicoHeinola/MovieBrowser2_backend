from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from models.base import Base


class ShowCategory(Base):
    __tablename__ = "show_categories"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("show_id", "name", name="uq_show_category"),)
