from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from models.base import Base
from models.website_tag import WebsiteTag


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)

    tags = relationship("WebsiteTag", cascade="all, delete-orphan", backref="website")

    def sync_tags(self, tags: list, db: Session):
        existing_tags_map = {tag.name: tag for tag in self.tags}
        tag_ids_to_delete = {tag.id for tag in self.tags}

        processed_tag_ids = set()

        for tag in tags:
            tag_name = tag.name if hasattr(tag, "name") else tag.get("name")
            tag_model = existing_tags_map.get(tag_name)

            if tag_model:
                processed_tag_ids.add(tag_model.id)
            else:
                new_tag = WebsiteTag(name=tag_name, website_id=self.id)
                db.add(new_tag)

        ids_to_actually_delete = tag_ids_to_delete - processed_tag_ids

        if ids_to_actually_delete:
            tags_to_remove = (
                db.query(WebsiteTag)
                .filter(
                    WebsiteTag.website_id == self.id,  # Ensure deletion is scoped to this website
                    WebsiteTag.id.in_(ids_to_actually_delete),
                )
                .all()
            )

            for tag_to_remove in tags_to_remove:
                db.delete(tag_to_remove)
