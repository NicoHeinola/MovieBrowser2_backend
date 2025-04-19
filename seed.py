from database import SessionLocal, engine
from models.models import Base, Movie

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    if db.query(Movie).count() == 0:
        movies = [
            Movie(title="The Matrix", director="Wachowski Sisters", year=1999),
            Movie(title="Inception", director="Christopher Nolan", year=2010),
            Movie(title="Interstellar", director="Christopher Nolan", year=2014),
        ]
        db.add_all(movies)
        db.commit()
    db.close()


if __name__ == "__main__":
    seed()
