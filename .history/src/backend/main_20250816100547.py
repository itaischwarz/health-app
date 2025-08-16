from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Food(BaseModel):
    name: str
    calories: int


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, name: str):
    return {"item_id": item_id, "food": name}


@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    return {"item_id": item_id, "food": name}