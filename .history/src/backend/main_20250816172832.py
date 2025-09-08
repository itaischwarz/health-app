from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from .db import engine, Base
from . import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


class Food(BaseModel):
    name: str
    calories: int



@app.get("/items/{food_name}")
def read_food_calories(food_name: str, calories: int):
    item = {"food name": food_name, "calories": calories}
    return item