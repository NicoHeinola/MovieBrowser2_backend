import json
from models.website import Website as WebsiteModel
from .seeder import Seeder


class WebsiteSeeder(Seeder):
    def seed(self, replace: bool = True, json_path="data/websites/default_websites.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            websites = json.load(f)
        for w in websites:
            existing = self.db.query(WebsiteModel).filter(WebsiteModel.url == w.get("url")).first()
            if existing:
                if not replace:
                    continue
                existing.title = w.get("title")
                existing.description = w.get("description")
                existing.icon = w.get("icon")
                existing.url = w.get("url")
            else:
                self.db.add(WebsiteModel(**w))
        self.db.commit()
