from database import SessionLocal
from seeders.user_seeder import UserSeeder
from sqlalchemy.orm import Session


def run_seeders(db: Session):
    user_seeder = UserSeeder(db)
    user_seeder.seed()  # Assuming a 'seed' method exists


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Running seeders...")
        run_seeders(db)
        print("Seeders finished.")
    except Exception as e:
        print(f"Seeding failed: {e}")
    finally:
        db.close()
