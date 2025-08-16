from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class Food(BaseModel):
    name: str
    calories: int



@app.get("/items/{item_id}")
def read_foo_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item