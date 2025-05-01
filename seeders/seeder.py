from sqlalchemy.orm import Session


class Seeder:
    """
    Base seeder class for seeding data into the database.
    """

    def __init__(self, db: Session):
        self.db: Session = db

    def seed(self):
        """
        Seed data into the database.
        """
        raise NotImplementedError("Subclasses must implement this method.")
