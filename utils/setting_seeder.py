import json
from models.setting import Setting as SettingModel


def seed_settings(db, json_path="data/settings/default_settings.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    for s in settings:
        existing = db.query(SettingModel).filter(SettingModel.key == s["key"]).first()
        if existing:
            existing.value = s["value"]
            existing.type = s["type"]
        else:
            db.add(SettingModel(**s))
    db.commit()
