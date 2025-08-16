



def calculate_remaining_calories(total_calories, consumed_calories):
    """
    Calculate the remaining calories based on total and consumed calories.
    
    Args:
        total_calories (int): The total calorie goal for the day.
        consumed_calories (int): The number of calories already consumed.
    
    Returns:
        int: The remaining calories to be consumed.
    """
    return max(0, total_calories - consumed_calories)