import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
