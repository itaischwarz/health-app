import random
import pandas as pd
import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from src.backend.db import engine

user_goal = {
    "calories": 2000,
    "protein": 120,
    "carbs": 250,
    "fat": 70
}

def score_meal_plan(meal_df, user_goal):
    totals = meal_df[["calories", "protein", "carbs", "fat"]].sum()
    
    # Weighted error score: the lower, the better
    score = (
        abs(user_goal["calories"] - totals["calories"]) +
        2 * abs(user_goal["protein"] - totals["protein"]) +
        abs(user_goal["carbs"] - totals["carbs"]) +
        2 * abs(user_goal["fat"] - totals["fat"])
    )
    return score


df = pd.read_sql("SELECT name, calories, protein, carbs, fat FROM food_items", engine)


def generate_best_plan(df, user_goal, trials=1000, meal_size=5):
    best_score = float("inf")
    best_plan = None
    
    for _ in range(trials):
        plan = df.sample(meal_size)
        score = score_meal_plan(plan, user_goal)
        if score < best_score:
            best_score = score
            best_plan = plan
    
    return best_plan

def generate_random_plan(df, meal_size=5):
    return df.sample(meal_size)


print("Best Meal Plan:", generate_best_plan(df, user_goal))