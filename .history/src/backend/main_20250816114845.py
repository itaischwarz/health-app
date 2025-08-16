from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class Food(BaseModel):
    name: str
    calories: int



@app.get("/items/{food_name}")
def read_food_calories(item_id: str, c: str):
    item = {"item_id": food_name, "needy": needy}
    return item