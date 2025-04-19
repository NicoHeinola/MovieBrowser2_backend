from fastapi import FastAPI
from routers import shows

app = FastAPI()

app.include_router(shows.router, prefix="/shows")
