import random

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
