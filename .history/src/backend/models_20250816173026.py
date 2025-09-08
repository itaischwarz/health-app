from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .db import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    name = Column(String, primary_key=True, index=True)
    calories = Column(Integer, nullable=False)
    protein = Column(Float, nullable=False)
    tags = Column(String)  # comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)