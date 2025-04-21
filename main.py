from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import shows
from routers import settings  # add this import

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shows.router, prefix="/shows")
app.include_router(settings.router, prefix="/settings")  # add this line
