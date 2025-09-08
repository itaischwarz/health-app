



def suggest_foods(current_calories, total_calories, maximum_calories, current_protein, total_protein):
    """
    Suggest foods based on the remaining calorie intake.
    
    Args:
        calories (int): The number of calories remaining for the day.
    
    Returns:
        list: A list of food suggestions.
    """
    # Placeholder for food suggestions logic
    if current_calories >= maximum_calories:
        return ["No more food suggestions, you've reached your calorie limit."]
    if current_protein >= total_protein and current_calories > maximum_calories:
        return ["No more protein suggestions, you've reached your protein limit."]
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