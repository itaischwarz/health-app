from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .db import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    name = Column(String, primary_key=True, index=True)
    calories = Column(Integer, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)  # comma-separated tags
    fat = Column(Float, nullable=False)  # comma-separated tags