from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from db import Base
from pydantic import BaseModel

class FoodItem(Base):
    __tablename__ = "foods"
    name = Column(String, primary_key=True, index=True)
    calories_per_100g = Column(Integer, nullable=False)
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)  # comma-separated tags
    fat_g = Column(Float, nullable=False)
      # comma-separated tags

class goals(BaseModel):
    
    target_calories: int
    target_protein: float = None
    target_carbs: float = None
    max_fat: float = None
    
class DietaryPrefrences(BaseModel):
    vegetarian: float = False
    vegan: float = False
    foods_to_disclude: list = None

class dayStatistics(BaseModel):
    current_calories: int
    current_protein: float = None
    current_carbs: float = None
    current_fat: float = None


