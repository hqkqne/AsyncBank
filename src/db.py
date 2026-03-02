import os
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from models import Base

load_dotenv()
DATABASE_URL = os.getenv("...")

engine = create_async_engine(..., echo = True)
AsyncSessionLocal = async_sessionmaker(bind = engine, expire_on_commit= Fasle)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Base is ready")
        yield
        print("get off")
        await engine.dispose()