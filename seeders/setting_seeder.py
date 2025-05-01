import json
from models.setting import Setting as SettingModel
from .seeder import Seeder


class SettingSeeder(Seeder):
    def seed(self, replace: bool = True, json_path="data/settings/default_settings.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        for s in settings:
            existing = self.db.query(SettingModel).filter(SettingModel.key == s["key"]).first()
            if existing and replace:
                existing.value = s["value"]
                existing.type = s["type"]
            else:
                self.db.add(SettingModel(**s))
        self.db.commit()
