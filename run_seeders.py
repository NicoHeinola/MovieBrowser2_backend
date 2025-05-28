import traceback
from dotenv import load_dotenv
from database import SessionLocal
from seeders.setting_seeder import SettingSeeder
from seeders.user_seeder import UserSeeder
from sqlalchemy.orm import Session

from seeders.website_seeder import WebsiteSeeder

load_dotenv(override=True)


def run_seeders(db: Session):
    user_seeder = UserSeeder(db)
    user_seeder.seed()

    setting_seeder = SettingSeeder(db)
    setting_seeder.seed(False)

    website_seeder = WebsiteSeeder(db)
    website_seeder.seed(False)


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Running seeders...")
        run_seeders(db)
        print("Seeders finished.")
    except Exception as e:
        print(f"Seeding failed: {traceback.format_exc()}")
    finally:
        db.close()
