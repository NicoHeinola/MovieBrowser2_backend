import json
from models.website import Website as WebsiteModel
from .seeder import Seeder


class WebsiteSeeder(Seeder):
    def seed(self, replace: bool = True, json_path="data/websites/default_websites.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            websites = json.load(f)
        for w in websites:
            tags = w.get("tags", [])
            w_data = {k: v for k, v in w.items() if k != "tags"}
            existing = self.db.query(WebsiteModel).filter(WebsiteModel.url == w.get("url")).first()
            if existing:
                if not replace:
                    continue
                existing.title = w.get("title")
                existing.description = w.get("description")
                existing.icon = w.get("icon")
                existing.url = w.get("url")
                existing.sync_tags(tags)
            else:
                website = WebsiteModel(**w_data)
                self.db.add(website)
                self.db.flush()
                website.sync_tags(tags)
        self.db.commit()
