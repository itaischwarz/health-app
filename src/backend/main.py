from typing import Union, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from db import engine, Base, SessionLocal
from models import FoodItem, goals, DietaryPrefrences, dayStatistics
from fastapi.middleware.cors import CORSMiddleware
from plan import create_plan
from fastapi.responses import JSONResponse


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",  # add both, since browser treats them differently
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/plan")
def get_plan(
    calories: int,
    protein: int,
    carbs: int,
    fat: int,
    total_calories: int,
    total_protein: int,
    total_carbs: int,
    total_fat: int,
    foods_list: int = None,
    prefs: Optional[str] = None,
):
    # print(foods[0])
    db = SessionLocal()
    foods = db.query(FoodItem).all()
    
    print(f"Found {len(foods)} foods in database")

    goals = {"target_calories": calories, "target_protein": protein, "target_carbs": carbs, "max_fat": fat}
    current_standing = {
        "current_calories": total_calories,
        "current_protein": total_protein,
        "current_carbs": total_carbs,
        "current_fat": total_fat,
    }
    
    plan = create_plan(goals, prefs, current_standing)
    plan_metrics, plan_solution = plan["metrics"], plan["plan"]
    print(f"Here are the plan metrics: {plan_metrics}")
    
    # Return JSON response instead of tuple
    return {
        "plan": plan_solution,
        "metrics": plan_metrics
    }
