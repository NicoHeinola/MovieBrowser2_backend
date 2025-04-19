from fastapi import FastAPI
from routers import movies

app = FastAPI()

app.include_router(movies.router, prefix="/movies", tags=["movies"])
