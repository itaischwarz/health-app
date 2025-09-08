



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
    suggestions = [
        {"name": "Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        {"name": "Broccoli", "calories": 55, "protein": 4.0, "carbs": 11.2, "fat": 0.6},
        {"name": "Brown Rice", "calories": 215, "protein": 5.0, "carbs": 45.8, "fat": 1.6},
        {"name": "Almonds", "calories": 579, "protein": 21.2, "carbs": 21.6, "fat": 49.9},
        {"name": "Greek Yogurt", "calories": 100, "protein": 10.0, "carbs": 6.0, "fat": 0.4},
        {''}
    
