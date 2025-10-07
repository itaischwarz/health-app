#!/usr/bin/env python3
"""
Script to populate the database with 119+ diverse foods including many carb-rich options
"""

from db import SessionLocal, engine
from models import FoodItem, Base
import os

def populate_foods():
    """Populate database with comprehensive food list"""
    
    # Create tables with new schema
    Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = SessionLocal()
    
    # Comprehensive food database with nutritional data per 100g
    foods_data = [
        # MEAT & PROTEIN (20 items)
        {"name": "Chicken Breast", "calories": 165, "protein_g": 31.0, "carbs_g": 0.0, "fat_g": 3.6, "category": "meat", "spread": False},
        {"name": "Chicken Thigh", "calories": 209, "protein_g": 26.0, "carbs_g": 0.0, "fat_g": 10.9, "category": "meat", "spread": False},
        {"name": "Ground Turkey", "calories": 189, "protein_g": 27.1, "carbs_g": 0.0, "fat_g": 8.0, "category": "meat", "spread": False},
        {"name": "Beef Sirloin", "calories": 250, "protein_g": 26.0, "carbs_g": 0.0, "fat_g": 15.0, "category": "meat", "spread": False},
        {"name": "Ground Beef (90% lean)", "calories": 176, "protein_g": 20.0, "carbs_g": 0.0, "fat_g": 10.0, "category": "meat", "spread": False},
        {"name": "Pork Tenderloin", "calories": 143, "protein_g": 26.0, "carbs_g": 0.0, "fat_g": 3.0, "category": "meat", "spread": False},
        {"name": "Salmon", "calories": 208, "protein_g": 25.4, "carbs_g": 0.0, "fat_g": 12.4, "category": "meat", "spread": False},
        {"name": "Tuna", "calories": 144, "protein_g": 30.0, "carbs_g": 0.0, "fat_g": 1.0, "category": "meat", "spread": False},
        {"name": "Cod", "calories": 82, "protein_g": 18.0, "carbs_g": 0.0, "fat_g": 0.7, "category": "meat", "spread": False},
        {"name": "Shrimp", "calories": 99, "protein_g": 24.0, "carbs_g": 0.0, "fat_g": 0.3, "category": "meat", "spread": False},
        {"name": "Eggs", "calories": 155, "protein_g": 13.0, "carbs_g": 1.1, "fat_g": 11.0, "category": "protein", "spread": False},
        {"name": "Egg Whites", "calories": 52, "protein_g": 11.0, "carbs_g": 0.7, "fat_g": 0.2, "category": "protein", "spread": False},
        {"name": "Tofu", "calories": 76, "protein_g": 8.0, "carbs_g": 1.9, "fat_g": 4.8, "category": "protein", "spread": False},
        {"name": "Tempeh", "calories": 192, "protein_g": 20.0, "carbs_g": 7.6, "fat_g": 10.8, "category": "protein", "spread": False},
        {"name": "Seitan", "calories": 370, "protein_g": 75.0, "carbs_g": 14.0, "fat_g": 1.9, "category": "protein", "spread": False},
        {"name": "Greek Yogurt", "calories": 59, "protein_g": 10.0, "carbs_g": 3.6, "fat_g": 0.4, "category": "dairy", "spread": False},
        {"name": "Cottage Cheese", "calories": 98, "protein_g": 11.0, "carbs_g": 3.4, "fat_g": 4.3, "category": "dairy", "spread": False},
        {"name": "Whey Protein", "calories": 370, "protein_g": 80.0, "carbs_g": 6.0, "fat_g": 3.0, "category": "protein", "spread": False},
        {"name": "Casein Protein", "calories": 370, "protein_g": 80.0, "carbs_g": 6.0, "fat_g": 3.0, "category": "protein", "spread": False},
        {"name": "Almonds", "calories": 579, "protein_g": 21.0, "carbs_g": 22.0, "fat_g": 50.0, "category": "nuts", "spread": False},
        
        # CARBS & GRAINS (25 items)
        {"name": "White Rice", "calories": 130, "protein_g": 2.7, "carbs_g": 28.0, "fat_g": 0.3, "category": "carbs", "spread": False},
        {"name": "Brown Rice", "calories": 111, "protein_g": 2.6, "carbs_g": 23.0, "fat_g": 0.9, "category": "carbs", "spread": False},
        {"name": "Basmati Rice", "calories": 130, "protein_g": 2.7, "carbs_g": 28.0, "fat_g": 0.3, "category": "carbs", "spread": False},
        {"name": "Jasmine Rice", "calories": 130, "protein_g": 2.7, "carbs_g": 28.0, "fat_g": 0.3, "category": "carbs", "spread": False},
        {"name": "Pasta (Cooked)", "calories": 131, "protein_g": 5.0, "carbs_g": 25.0, "fat_g": 1.1, "category": "carbs", "spread": False},
        {"name": "Whole Wheat Pasta", "calories": 124, "protein_g": 5.0, "carbs_g": 25.0, "fat_g": 1.1, "category": "carbs", "spread": False},
        {"name": "Oats", "calories": 389, "protein_g": 16.9, "carbs_g": 66.3, "fat_g": 6.9, "category": "carbs", "spread": False},
        {"name": "Oatmeal", "calories": 68, "protein_g": 2.4, "carbs_g": 12.0, "fat_g": 1.4, "category": "carbs", "spread": False},
        {"name": "Quinoa", "calories": 120, "protein_g": 4.4, "carbs_g": 22.0, "fat_g": 1.9, "category": "carbs", "spread": False},
        {"name": "Barley", "calories": 352, "protein_g": 12.5, "carbs_g": 73.5, "fat_g": 2.3, "category": "carbs", "spread": False},
        {"name": "Bulgur", "calories": 83, "protein_g": 3.1, "carbs_g": 18.6, "fat_g": 0.2, "category": "carbs", "spread": False},
        {"name": "Whole Wheat Bread", "calories": 247, "protein_g": 13.4, "carbs_g": 41.3, "fat_g": 4.2, "category": "carbs", "spread": False},
        {"name": "White Bread", "calories": 265, "protein_g": 9.0, "carbs_g": 49.0, "fat_g": 3.2, "category": "carbs", "spread": False},
        {"name": "Sourdough Bread", "calories": 289, "protein_g": 11.0, "carbs_g": 56.0, "fat_g": 2.0, "category": "carbs", "spread": False},
        {"name": "Bagel", "calories": 257, "protein_g": 10.1, "carbs_g": 50.9, "fat_g": 1.7, "category": "carbs", "spread": False},
        {"name": "Tortilla (Flour)", "calories": 218, "protein_g": 5.7, "carbs_g": 44.6, "fat_g": 2.3, "category": "carbs", "spread": False},
        {"name": "Tortilla (Corn)", "calories": 218, "protein_g": 5.7, "carbs_g": 44.6, "fat_g": 2.3, "category": "carbs", "spread": False},
        {"name": "Sweet Potato", "calories": 86, "protein_g": 1.6, "carbs_g": 20.1, "fat_g": 0.1, "category": "carbs", "spread": False},
        {"name": "White Potato", "calories": 77, "protein_g": 2.0, "carbs_g": 17.5, "fat_g": 0.1, "category": "carbs", "spread": False},
        {"name": "Yam", "calories": 118, "protein_g": 1.5, "carbs_g": 27.9, "fat_g": 0.2, "category": "carbs", "spread": False},
        {"name": "Corn", "calories": 86, "protein_g": 3.3, "carbs_g": 19.0, "fat_g": 1.2, "category": "carbs", "spread": False},
        {"name": "Popcorn", "calories": 387, "protein_g": 12.9, "carbs_g": 77.8, "fat_g": 4.5, "category": "carbs", "spread": False},
        {"name": "Crackers", "calories": 421, "protein_g": 9.0, "carbs_g": 74.0, "fat_g": 9.0, "category": "carbs", "spread": False},
        {"name": "Cereal (General)", "calories": 378, "protein_g": 7.0, "carbs_g": 85.0, "fat_g": 1.0, "category": "carbs", "spread": False},
        {"name": "Granola", "calories": 471, "protein_g": 10.0, "carbs_g": 64.0, "fat_g": 20.0, "category": "carbs", "spread": False},
        
        # FRUITS (20 items)
        {"name": "Banana", "calories": 89, "protein_g": 1.1, "carbs_g": 22.8, "fat_g": 0.3, "category": "fruits", "spread": False},
        {"name": "Apple", "calories": 52, "protein_g": 0.3, "carbs_g": 13.8, "fat_g": 0.2, "category": "fruits", "spread": False},
        {"name": "Orange", "calories": 47, "protein_g": 0.9, "carbs_g": 11.8, "fat_g": 0.1, "category": "fruits", "spread": False},
        {"name": "Blueberries", "calories": 57, "protein_g": 0.7, "carbs_g": 14.5, "fat_g": 0.3, "category": "fruits", "spread": False},
        {"name": "Strawberries", "calories": 32, "protein_g": 0.7, "carbs_g": 7.7, "fat_g": 0.3, "category": "fruits", "spread": False},
        {"name": "Raspberries", "calories": 52, "protein_g": 1.2, "carbs_g": 11.9, "fat_g": 0.7, "category": "fruits", "spread": False},
        {"name": "Blackberries", "calories": 43, "protein_g": 1.4, "carbs_g": 9.6, "fat_g": 0.5, "category": "fruits", "spread": False},
        {"name": "Grapes", "calories": 62, "protein_g": 0.6, "carbs_g": 16.0, "fat_g": 0.2, "category": "fruits", "spread": False},
        {"name": "Mango", "calories": 60, "protein_g": 0.8, "carbs_g": 15.0, "fat_g": 0.4, "category": "fruits", "spread": False},
        {"name": "Pineapple", "calories": 50, "protein_g": 0.5, "carbs_g": 13.1, "fat_g": 0.1, "category": "fruits", "spread": False},
        {"name": "Watermelon", "calories": 30, "protein_g": 0.6, "carbs_g": 7.6, "fat_g": 0.2, "category": "fruits", "spread": False},
        {"name": "Cantaloupe", "calories": 34, "protein_g": 0.8, "carbs_g": 8.2, "fat_g": 0.2, "category": "fruits", "spread": False},
        {"name": "Peach", "calories": 39, "protein_g": 0.9, "carbs_g": 9.5, "fat_g": 0.3, "category": "fruits", "spread": False},
        {"name": "Pear", "calories": 57, "protein_g": 0.4, "carbs_g": 15.2, "fat_g": 0.1, "category": "fruits", "spread": False},
        {"name": "Cherries", "calories": 63, "protein_g": 1.1, "carbs_g": 16.0, "fat_g": 0.2, "category": "fruits", "spread": False},
        {"name": "Kiwi", "calories": 61, "protein_g": 1.1, "carbs_g": 14.7, "fat_g": 0.5, "category": "fruits", "spread": False},
        {"name": "Avocado", "calories": 160, "protein_g": 2.0, "carbs_g": 8.5, "fat_g": 14.7, "category": "fruits", "spread": False},
        {"name": "Coconut", "calories": 354, "protein_g": 3.3, "carbs_g": 15.2, "fat_g": 33.5, "category": "fruits", "spread": False},
        {"name": "Dates", "calories": 277, "protein_g": 1.8, "carbs_g": 75.0, "fat_g": 0.2, "category": "fruits", "spread": False},
        {"name": "Raisins", "calories": 299, "protein_g": 3.1, "carbs_g": 79.2, "fat_g": 0.5, "category": "fruits", "spread": False},
        
        # VEGETABLES (20 items)
        {"name": "Broccoli", "calories": 34, "protein_g": 2.8, "carbs_g": 6.6, "fat_g": 0.4, "category": "vegetables", "spread": False},
        {"name": "Spinach", "calories": 23, "protein_g": 2.9, "carbs_g": 3.6, "fat_g": 0.4, "category": "vegetables", "spread": False},
        {"name": "Kale", "calories": 49, "protein_g": 4.3, "carbs_g": 8.8, "fat_g": 0.9, "category": "vegetables", "spread": False},
        {"name": "Lettuce", "calories": 15, "protein_g": 1.4, "carbs_g": 2.9, "fat_g": 0.2, "category": "vegetables", "spread": False},
        {"name": "Carrots", "calories": 41, "protein_g": 0.9, "carbs_g": 9.6, "fat_g": 0.2, "category": "vegetables", "spread": False},
        {"name": "Bell Peppers", "calories": 31, "protein_g": 1.0, "carbs_g": 7.3, "fat_g": 0.3, "category": "vegetables", "spread": False},
        {"name": "Tomatoes", "calories": 18, "protein_g": 0.9, "carbs_g": 3.9, "fat_g": 0.2, "category": "vegetables", "spread": False},
        {"name": "Cucumber", "calories": 16, "protein_g": 0.7, "carbs_g": 4.0, "fat_g": 0.1, "category": "vegetables", "spread": False},
        {"name": "Onions", "calories": 40, "protein_g": 1.1, "carbs_g": 9.3, "fat_g": 0.1, "category": "vegetables", "spread": False},
        {"name": "Garlic", "calories": 149, "protein_g": 6.4, "carbs_g": 33.1, "fat_g": 0.5, "category": "vegetables", "spread": False},
        {"name": "Mushrooms", "calories": 22, "protein_g": 3.1, "carbs_g": 3.3, "fat_g": 0.3, "category": "vegetables", "spread": False},
        {"name": "Asparagus", "calories": 20, "protein_g": 2.2, "carbs_g": 3.9, "fat_g": 0.1, "category": "vegetables", "spread": False},
        {"name": "Brussels Sprouts", "calories": 43, "protein_g": 3.4, "carbs_g": 8.9, "fat_g": 0.3, "category": "vegetables", "spread": False},
        {"name": "Cauliflower", "calories": 25, "protein_g": 1.9, "carbs_g": 5.0, "fat_g": 0.3, "category": "vegetables", "spread": False},
        {"name": "Cabbage", "calories": 25, "protein_g": 1.3, "carbs_g": 5.8, "fat_g": 0.1, "category": "vegetables", "spread": False},
        {"name": "Zucchini", "calories": 17, "protein_g": 1.2, "carbs_g": 3.4, "fat_g": 0.2, "category": "vegetables", "spread": False},
        {"name": "Eggplant", "calories": 25, "protein_g": 1.0, "carbs_g": 5.9, "fat_g": 0.2, "category": "vegetables", "spread": False},
        {"name": "Green Beans", "calories": 31, "protein_g": 1.8, "carbs_g": 7.0, "fat_g": 0.1, "category": "vegetables", "spread": False},
        {"name": "Peas", "calories": 81, "protein_g": 5.4, "carbs_g": 14.5, "fat_g": 0.4, "category": "vegetables", "spread": False},
        {"name": "Artichoke", "calories": 47, "protein_g": 3.3, "carbs_g": 10.5, "fat_g": 0.2, "category": "vegetables", "spread": False},
        
        # LEGUMES (10 items)
        {"name": "Black Beans", "calories": 132, "protein_g": 8.9, "carbs_g": 23.7, "fat_g": 0.5, "category": "legumes", "spread": False},
        {"name": "Kidney Beans", "calories": 127, "protein_g": 8.7, "carbs_g": 22.8, "fat_g": 0.5, "category": "legumes", "spread": False},
        {"name": "Chickpeas", "calories": 164, "protein_g": 8.9, "carbs_g": 27.4, "fat_g": 2.6, "category": "legumes", "spread": False},
        {"name": "Lentils", "calories": 116, "protein_g": 9.0, "carbs_g": 20.1, "fat_g": 0.4, "category": "legumes", "spread": False},
        {"name": "Pinto Beans", "calories": 143, "protein_g": 9.0, "carbs_g": 26.2, "fat_g": 0.6, "category": "legumes", "spread": False},
        {"name": "Navy Beans", "calories": 140, "protein_g": 8.2, "carbs_g": 26.1, "fat_g": 0.6, "category": "legumes", "spread": False},
        {"name": "Lima Beans", "calories": 115, "protein_g": 7.8, "carbs_g": 20.9, "fat_g": 0.4, "category": "legumes", "spread": False},
        {"name": "Split Peas", "calories": 118, "protein_g": 8.3, "carbs_g": 21.1, "fat_g": 0.4, "category": "legumes", "spread": False},
        {"name": "Edamame", "calories": 122, "protein_g": 11.9, "carbs_g": 9.9, "fat_g": 5.2, "category": "legumes", "spread": False},
        {"name": "Hummus", "calories": 166, "protein_g": 7.9, "carbs_g": 14.3, "fat_g": 9.6, "category": "legumes", "spread": True},
        
        # DAIRY (10 items)
        {"name": "Milk (2%)", "calories": 50, "protein_g": 3.3, "carbs_g": 4.7, "fat_g": 2.0, "category": "dairy", "spread": False},
        {"name": "Milk (Whole)", "calories": 61, "protein_g": 3.2, "carbs_g": 4.7, "fat_g": 3.3, "category": "dairy", "spread": False},
        {"name": "Almond Milk", "calories": 17, "protein_g": 0.6, "carbs_g": 0.6, "fat_g": 1.1, "category": "dairy", "spread": False},
        {"name": "Soy Milk", "calories": 33, "protein_g": 2.9, "carbs_g": 1.8, "fat_g": 1.9, "category": "dairy", "spread": False},
        {"name": "Coconut Milk", "calories": 230, "protein_g": 2.3, "carbs_g": 5.5, "fat_g": 23.8, "category": "dairy", "spread": False},
        {"name": "Cheese (Cheddar)", "calories": 403, "protein_g": 25.0, "carbs_g": 1.3, "fat_g": 33.1, "category": "dairy", "spread": False},
        {"name": "Mozzarella", "calories": 280, "protein_g": 22.2, "carbs_g": 2.2, "fat_g": 22.4, "category": "dairy", "spread": False},
        {"name": "Butter", "calories": 717, "protein_g": 0.9, "carbs_g": 0.1, "fat_g": 81.1, "category": "dairy", "spread": True},
        {"name": "Cream Cheese", "calories": 342, "protein_g": 6.2, "carbs_g": 4.1, "fat_g": 34.4, "category": "dairy", "spread": True},
        {"name": "Sour Cream", "calories": 198, "protein_g": 2.8, "carbs_g": 4.6, "fat_g": 19.4, "category": "dairy", "spread": True},
        
        # NUTS & SEEDS (10 items)
        {"name": "Walnuts", "calories": 654, "protein_g": 15.2, "carbs_g": 13.7, "fat_g": 65.2, "category": "nuts", "spread": False},
        {"name": "Cashews", "calories": 553, "protein_g": 18.2, "carbs_g": 30.2, "fat_g": 43.8, "category": "nuts", "spread": False},
        {"name": "Pistachios", "calories": 560, "protein_g": 20.2, "carbs_g": 27.2, "fat_g": 45.3, "category": "nuts", "spread": False},
        {"name": "Pecans", "calories": 691, "protein_g": 9.2, "carbs_g": 13.9, "fat_g": 72.0, "category": "nuts", "spread": False},
        {"name": "Hazelnuts", "calories": 628, "protein_g": 15.0, "carbs_g": 16.7, "fat_g": 60.8, "category": "nuts", "spread": False},
        {"name": "Chia Seeds", "calories": 486, "protein_g": 16.5, "carbs_g": 42.1, "fat_g": 30.7, "category": "nuts", "spread": False},
        {"name": "Flax Seeds", "calories": 534, "protein_g": 18.3, "carbs_g": 28.9, "fat_g": 42.2, "category": "nuts", "spread": False},
        {"name": "Sunflower Seeds", "calories": 584, "protein_g": 20.8, "carbs_g": 20.0, "fat_g": 51.5, "category": "nuts", "spread": False},
        {"name": "Pumpkin Seeds", "calories": 559, "protein_g": 30.2, "carbs_g": 10.7, "fat_g": 49.1, "category": "nuts", "spread": False},
        {"name": "Peanut Butter", "calories": 588, "protein_g": 25.1, "carbs_g": 19.6, "fat_g": 50.4, "category": "nuts", "spread": True},
        
        # FATS & OILS (8 items)
        {"name": "Olive Oil", "calories": 884, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        {"name": "Coconut Oil", "calories": 862, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        {"name": "Avocado Oil", "calories": 884, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        {"name": "Canola Oil", "calories": 884, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        {"name": "Sesame Oil", "calories": 884, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        {"name": "Ghee", "calories": 900, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": True},
        {"name": "Lard", "calories": 902, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        {"name": "Tallow", "calories": 902, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "category": "fats", "spread": False},
        
        # SWEETENERS & SPREADS (6 items)
        {"name": "Honey", "calories": 304, "protein_g": 0.3, "carbs_g": 82.4, "fat_g": 0.0, "category": "sweeteners", "spread": True},
        {"name": "Maple Syrup", "calories": 260, "protein_g": 0.0, "carbs_g": 67.0, "fat_g": 0.0, "category": "sweeteners", "spread": True},
        {"name": "Agave", "calories": 310, "protein_g": 0.0, "carbs_g": 76.0, "fat_g": 0.0, "category": "sweeteners", "spread": True},
        {"name": "Jam", "calories": 278, "protein_g": 0.4, "carbs_g": 69.0, "fat_g": 0.1, "category": "sweeteners", "spread": True},
        {"name": "Jelly", "calories": 266, "protein_g": 0.0, "carbs_g": 69.0, "fat_g": 0.0, "category": "sweeteners", "spread": True},
        {"name": "Nutella", "calories": 539, "protein_g": 6.3, "carbs_g": 57.5, "fat_g": 30.9, "category": "sweeteners", "spread": True},
    ]
    
    try:
        # Clear existing foods
        db.query(FoodItem).delete()
        
        # Add all foods to database
        for food_data in foods_data:
            new_food = FoodItem(**food_data)
            db.add(new_food)
        
        # Commit changes
        db.commit()
        print(f"Successfully added {len(foods_data)} foods to the database!")
        
        # Show summary by category
        categories = {}
        for food_data in foods_data:
            cat = food_data["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nFood count by category:")
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} foods")
        
        # Show carb-rich foods specifically
        carb_foods = [f for f in foods_data if f["category"] == "carbs"]
        print(f"\nCarb-rich foods: {len(carb_foods)} items")
        for food in carb_foods[:10]:  # Show first 10
            print(f"  - {food['name']}: {food['carbs_g']}g carbs")
        if len(carb_foods) > 10:
            print(f"  ... and {len(carb_foods) - 10} more carb foods")
        
    except Exception as e:
        print(f"Error adding foods: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_foods()
