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
    


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, food: Food):
    return {"item_id": item_id, "food": food}