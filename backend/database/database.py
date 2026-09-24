"""Database connection and session factory."""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/roboteleop.db")

async def init_db():
    # Database initialization placeholder
    pass
