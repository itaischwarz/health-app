from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class Food(BaseModel):
    name: str
    calories: int
class FoodType(str, Enum):
    fruit = "fruit"
    pasta = "pasta"
    steak = "steak"


@app.get("/foods/{food_type}")
def get_foods(food_type: FoodType):
    if food_type == FoodType.fruit:
        return {"food": "apple", "type": food_type, "enum_value": food_type.value}
    elif food_type == FoodType.pasta:
        return {"food": "spaghetti", "type": food_type, "enum_value": food_type.value}
    elif food_type == FoodType.steak:
        return {"food": "ribeye", "type": food_type}
    else:
        return {"error": "Unknown food type"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, food: Food):
    return {"item_id": item_id, "food": food}