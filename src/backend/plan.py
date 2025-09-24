from models import FoodItem, goals, DietaryPrefrences, dayStatistics
from sqlalchemy.orm import Session
from db import SessionLocal
import psycopg2
import pandas as pd
from ortools.sat.python import cp_model
import numpy as np
import math

def create_plan(goals_dict, prefs, currentStanding):
    # Connect to PostgreSQL database "food_db" with read-only user "viewer"
    connection = psycopg2.connect(dbname="food_db", user="viewer", host="localhost", port="5432")

    # Load calories, protein, carbs, fat per 100g from foods table into a DataFrame
    df = pd.read_sql("SELECT calories_per_100g, protein_g, carbs_g, fat_g, category FROM foods;", connection)

    df = pd.get_dummies(df, columns=["category"], dtype=int)
    # df = pd.get_dummies(df, columns=["category"], dtype=int)


    # Convert DataFrame to numpy array (rows = foods, cols = nutrients)
    A = df.to_numpy()

    # Daily nutrition targets (object from your goals dataclass/model)
    dailyGoals = goals(**goals_dict)

    # Current day's nutrition totals (object from your dayStatistics dataclass/model)
    currentDayStatistics = dayStatistics(**currentStanding)



    # Remaining targets = daily goal – current intake
    remaining_calories = dailyGoals.target_calories - currentDayStatistics.current_calories
    remaining_protein = dailyGoals.target_protein - currentDayStatistics.current_protein
    remaining_carbs   = dailyGoals.target_carbs - currentDayStatistics.current_carbs
    remaining_fat     = dailyGoals.max_fat - currentDayStatistics.current_fat


    total_items = 199 

    # Number of nutrient categories (4: calories, protein, carbs, fat)
    categories = 11

    # Upper bound on number of distinct foods chosen (heuristic: remaining_calories/10)
    distinct_items = int(remaining_calories / 180)

    # Target vector [remaining calories, protein, carbs, fat]
    t = np.array([remaining_calories, remaining_protein, remaining_carbs, remaining_fat])  # last three for categories

    # Weight vector: how much to prioritize each nutrient deviation in optimization
    w = np.array([1.0, 20.0, 20.0, 30.0])  # protein, carbs, fat deviations penalized more

    # Upper bounds for how many units of each food can be chosen (here: 200 items max, 2 units each)
    U = 199 * [2]   

    print("HERE")

    # Number of food items

    # Create CP-SAT model
    m = cp_model.CpModel()

    # Decision vars: how many units of each food (0..U[i])
    x = [m.NewIntVar(0, U[i], f"x_{i}") for i in range(total_items)]

    y = [m.NewIntVar(0, 10000, f"y_{k}") for k in range(categories)]
    

    # Boolean vars: whether a food is selected at all
    z = [m.NewBoolVar(f"z_{i}") for i in range(total_items)]


    m.Add(y[5] > 0)
    m.Add(y[6] > 0)
    m.Add(y[8] > 0)
    # m.Add(y[8] <= 2)
    m.Add(y[9] > 0)
    m.Add(y[10] > 0)




    for i in range(total_items):
        m.Add(x[i] >= 0).OnlyEnforceIf(z[i])
        m.Add(x[i] == 0).OnlyEnforceIf(z[i].Not())


    # Constraint: total distinct foods used <= distinct_items
    m.Add(sum(z) <= distinct_items)



    # Nutrient totals: y[k] = sum of (nutrient value of food * servings of food)
    for k in range((categories)):
        m.Add(y[k] == sum(int(A[i, k]) * x[i] for i in range(total_items)))

    # Deviation variables (positive and negative) for each nutrient target
    dev_pos = [m.NewIntVar(0, 10000, f"dpos_{k}") for k in range(categories)]
    dev_neg = [m.NewIntVar(0, 10000, f"dneg_{k}") for k in range(categories)]

    print(total_items)

    # Constraint: (actual - target) = (positive deviation - negative deviation)
    for k in range(4):
        m.Add(y[k] - int(t[k]) == dev_pos[k] - dev_neg[k])

    # Objective: Minimize weighted sum of deviations (try to hit targets closely)
    m.Minimize(sum(int(w[k]) * (dev_pos[k] + dev_neg[k]) for k in range(4)))

    # Create solver
    solver = cp_model.CpSolver()

    # Solve optimization model
    status = solver.Solve(m)

    # If no feasible solution, return None
    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        return {"plan": None, "metrics": None}

    # Limit solver runtime to 5s (⚠️ this line should usually go BEFORE Solve())
    solver.parameters.max_time_in_seconds = 5

    # Load food names to map variables back to food items
    foods_df = pd.read_sql("SELECT name FROM foods", connection)
    foods = foods_df.to_numpy()
    # Solution: servings of each food
    solution = {f"{foods[i]}": solver.Value(x[i]) for i in range(len(x) ) if solver.Value(x[i]) > 0}
    # Metrics: actual totals for [calories, protein, carbs, fat]
    metrics  = [solver.Value(y[k]) for k in range(len(y)) ]
    print(sum(solution.values()))
    return {"plan": solution, "metrics": metrics}


print(create_plan({'target_calories': 2000, 'target_protein': 90.0, 'target_carbs': 150.0, 'max_fat': 50.0}, None, {'current_calories': 0, 'current_protein': 0, 'current_carbs': 0, 'current_fat': 0}))


# def create_meal(target_calories, target_protein, target_carbs):


