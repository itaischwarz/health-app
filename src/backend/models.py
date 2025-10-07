from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from datetime import datetime
from db import Base
from pydantic import BaseModel

class FoodItem(Base):
    __tablename__ = "foods"
    name = Column(String, primary_key=True, index=True)
    calories = Column(Integer, nullable=False)
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    category = Column(String, nullable=True)  # Food categories like "carbs", "meat", "dairy"
    spread = Column(Boolean, nullable=True)   # Whether item is a spread

class goals(BaseModel):
    
    target_calories: int
    target_protein: float
    target_carbs: float
    max_fat: float
    
class DietaryPrefrences(BaseModel):
    vegetarian: float = False
    vegan: float = False
    foods_to_disclude: list = None

class dayStatistics(BaseModel):
    current_calories: int
    current_protein: float = None
    current_carbs: float = None
    current_fat: float = None


