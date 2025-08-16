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

fake_foods = [
    {"name": "apple", "calories": 95, "type": FoodType.fruit},
    {"name": "spaghetti", "calories": 200, "type": FoodType.pasta},
    {"name": "ribeye", "calories": 300, "type": FoodType.steak},
]


@app.get("/foods")
def get_foods_list(skip: int = 0, limit: int = 3):
    return fake_foods[skip: skip+limit]
@app.get("/foods/{food_type}")
def get_foods(food_type: FoodType):
    if food_type == FoodType.fruit:
        return {"food": "apple", "type": food_type, "enum_value": food_type.value}
    elif food_type == FoodType.pasta:
        return {"food": "spaghetti", "type": food_type, "enum_value": food_type.value}
    elif food_type == FoodType.steak:
        return {"food": "ribeye", "type": food_type, "enum_value": food_type.value}
    else:
        return {"error": "Unknown food type"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"query": q})
    if not short:
        item.update({"description": "This is a long description of the item."})
    return item


@app.get("/user/{user_id}/items/{item_id}")
def read_item_name(item_id: int, user_id: int, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "name": "Item Name


@app.put("/items/{item_id}")
def update_item(item_id: int, food: Food):
    return {"item_id": item_id, "food": food}