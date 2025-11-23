import logging
from fastapi import FastAPI
from app.routers import registration, authentication
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.database import init_models
from app.services import FaceRecognition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Student Face Recognition API",
    description="Talabalarning yuzini aniqlash uchun API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(registration.router)
app.include_router(authentication.router)

face_recognition = FaceRecognition(threshold=0.65)

@app.on_event("startup")
async def on_startup():
    logger.info("Creating database tables...")
    await init_models()
    logger.info("Database tables created.")


@app.get("/")
async def root():
    return {"message": "Face Recognition API ishlamoqda!"}