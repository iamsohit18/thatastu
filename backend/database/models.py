"""Database models for metadata persistence."""
from typing import Optional
from datetime import datetime, timezone

try:
    from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()

    class EpisodeRecord(Base):
        __tablename__ = "episodes"
        episode_id = Column(String(64), primary_key=True, index=True)
        task_id = Column(String(64), index=True)
        operator_id = Column(String(64))
        robot_id = Column(String(64))
        leader_id = Column(String(64))
        start_time = Column(String(64))
        end_time = Column(String(64), nullable=True)
        duration_seconds = Column(Float, default=0.0)
        total_frames = Column(Integer, default=0)
        validation_status = Column(String(32), default="PENDING")
        human_review_status = Column(String(32), default="UNREVIEWED")
        outcome = Column(String(32), default="success")

except ImportError:
    # Lightweight fallback if SQLAlchemy is not installed
    class Base:
        pass
    class EpisodeRecord:
        pass
