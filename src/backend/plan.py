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
    df = pd.read_sql("SELECT name ,calories, protein_g, carbs_g, fat_g, category, spread FROM foods;", connection)

    # Normalize spread column values
    df["spread"] = df["spread"].replace({"Yes": 1, "No": 0, True: 1, False: 0}).fillna(0).astype(int)

    # Ensure category comparisons are safe (lowercase)
    df["category"] = df["category"].astype(str)

    # find the correct name column (some of your code used 'food_name' vs 'name')
    if "food_name" in df.columns:
        name_col = "food_name"
    else:
        name_col = "name"

    # df_spreads: dairy items (case-insensitive)
    df_spreads = df[df["spread"] == 1]
    print(df_spreads)

    # df_breads using the detected name column
    df_breads = df[df[name_col].astype(str).str.lower().str.contains(r"bread|bagel", na=False)]

    # Apply preferences (use name_col consistently and lowercase category checks)
    if "vegetarian" in prefs:
        df = df[~df["category"].str.lower().eq("meat")]
    if "vegan" in prefs:
        df = df[
            (~df["category"].str.lower().eq("meat")) &
            (~df["category"].str.lower().eq("dairy")) &
            (~df[name_col].str.lower().str.contains(r"\begg\b", na=False))
        ]
    if "kosher" in prefs or "halal" in prefs:
        df = df[
            ~df[name_col].str.contains(r"\b(pork|ham|bacon)\b", case=False, na=False)
        ]

    # one-hot categories (this will add columns after the 4 nutrient columns)
    df = pd.get_dummies(df, columns=["category"], dtype=int)

    # Convert DataFrame to numpy array (rows = foods, cols = nutrients + other columns)
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

    # --- SMALL FIX: align total_items with dataframe length (was hardcoded) ---
    total_items = len(df)

    # Number of nutrient categories (4: calories, protein, carbs, fat)
    print(df.head())
    categories = 4

    # columns variable you had; keep but it's not used for nutrient sums now
    columns = df.iloc[:,1:].shape[1]
    print("columns", columns)
    t = np.array([remaining_calories, remaining_protein, remaining_carbs, remaining_fat])  # last three for categories
    w = np.array([1.0, 1.0, 1.0, 1.0])  # protein, carbs, fat deviations penalized more
    U = [2] * total_items
    m = cp_model.CpModel()
    x = [m.NewIntVar(0, U[i], f"x_{i}") for i in range(total_items)]
    # --- y should represent the four nutrient totals (calories, protein, carbs, fat) ---
    y = [m.NewIntVar(0, 1000000, f"y_{k}") for k in range(columns)]
    z = [m.NewBoolVar(f"z_{i}") for i in range(total_items)]
    pos_map = {idx: i for i, idx in enumerate(df.index)}
    df_breads = df[df[name_col].astype(str).str.lower().str.contains(r"bread|bagel", na=False)]
    bread_positions = [pos_map[idx] for idx in df_breads.index if idx in pos_map]
    spread_positions = [df.index.get_loc(idx) for idx in df_spreads.index if idx in df.index]
    spread_count = len(spread_positions)
    # enforce bread-servings == spread_count (if impossible, return None early)
    if spread_count > 0 and len(bread_positions) == 0:
        # no breads available but spread required -> infeasible catalog
        return {"plan": None, "metrics": {"error": "spread_count > 0 but no breads available in catalog after prefs"}}

    if len(bread_positions) > 0:
        m.Add(sum(x[p] for p in bread_positions) == sum(x[s] for s in spread_positions))

    for i in range(total_items):
        m.Add(x[i] >= 1).OnlyEnforceIf(z[i])
        m.Add(x[i] == 0).OnlyEnforceIf(z[i].Not())

    total = []
    for j in range(categories+1, columns):
        total.append(sum(df.iloc[i, j] * z[i] for i in range(total_items)))

    for i in range(0, columns-categories-1):
        m.Add(total[i] >= 1)
        m.Add(total[i] <= 2)

    for i in range(total_items):
        m.Add(x[i] >= 0)
    # --- Nutrient totals: compute from explicit nutrient columns (safe and clear) ---
    # Use columns explicitly to avoid mis-indexing (A contains many columns after get_dummies)
    # We expect df has columns: name, calories, protein_g, carbs_g, fat_g, ... (possibly other dummies)
    nutrient_cols = ['calories', 'protein_g', 'carbs_g', 'fat_g']
    for k in range(categories):
        coeffs = []
        for i in range(total_items):
            # safe extraction: if column missing fallback to 0
            try:
                coeff = int(df.iloc[i][nutrient_cols[k]])
            except Exception:
                coeff = 0
            coeffs.append(coeff)
        m.Add(y[k] == sum(coeffs[i] * x[i] for i in range(total_items)))

    # Deviation variables (positive and negative) for each nutrient target
    dev_pos = [m.NewIntVar(0, 1000000, f"dpos_{k}") for k in range(categories)]
    dev_neg = [m.NewIntVar(0, 1000000, f"dneg_{k}") for k in range(categories)]

    print(total_items)

    # Constraint: (actual - target) = (positive deviation - negative deviation)
    for k in range(categories):
        m.Add(y[k] - int(t[k]) == dev_pos[k] - dev_neg[k])

    # Objective: Minimize weighted sum of deviations (try to hit targets closely)
    # scale weights into integers for CP-SAT
    scale = 100
    int_w = [int(w[k] * scale) for k in range(categories)]
    m.Minimize(sum(int_w[k] * (dev_pos[k] + dev_neg[k]) for k in range(categories)))

    # Create solver and set time limit BEFORE Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5
    status = solver.Solve(m)

    # If no feasible solution, return None
    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        return {"plan": None, "metrics": None}

    # Load food names to map variables back to food items
    foods = df.iloc[:, 0].to_numpy()
    # Solution: servings of each food
    solution = {f"{foods[i]}": solver.Value(x[i]) for i in range(len(x)) if solver.Value(x[i]) > 0}
    # Metrics: actual totals for [calories, protein, carbs, fat]
    metrics  = [solver.Value(y[k]) for k in range(categories)]



    return {"plan": solution, "metrics": metrics}

print(create_plan({'target_calories': 2000, 'target_protein': 90.0, 'target_carbs': 150.0, 'max_fat': 50.0}, {}, {'current_calories': 0, 'current_protein': 0, 'current_carbs': 0, 'current_fat': 0}))


# def create_meal(target_calories, target_protein, target_carbs):


