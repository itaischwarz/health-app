from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    name = Column(String, primary_key=True, index=True)
    calories = Column(Integer, nullable=False)
    title = Column(Float)
    tags = Column(String)  # comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)