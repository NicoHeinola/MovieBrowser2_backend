from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from models.base import Base


class WebsiteTag(Base):
    __tablename__ = "website_tags"
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("website_id", "name", name="uq_website_tag"),)
