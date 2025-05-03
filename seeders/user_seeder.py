import os
from models.user import User
from seeders.seeder import Seeder
from utils import auth


class UserSeeder(Seeder):
    def seed(self):
        ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
        ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

        if not ADMIN_PASSWORD or not ADMIN_USERNAME:
            return

        admin = self.db.query(User).filter(User.username == ADMIN_USERNAME).first()

        if not admin:
            admin = User(username=ADMIN_USERNAME)

        admin.password = auth.get_password_hash(ADMIN_PASSWORD)
        admin.username = ADMIN_USERNAME
        admin.is_admin = True

        self.db.add(admin)
        self.db.commit()
