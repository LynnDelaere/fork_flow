from utils import load_recipes, filter_recipes_by_type
import random
from typing import List, Dict

recipes_file_path = './recipes.json'

def generate_meal_plan() -> Dict[str, Dict[str, Dict]]:
    recipes = load_recipes(recipes_file_path)
    plan = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    meal_types = ['Breakfast', 'Lunch', 'Dinner']
    for day in days:
        plan[day] = {}
        for meal in meal_types:
            # Randomly select a recipe for each meal type
            available_recipes = filter_recipes_by_type(recipes, meal)
            if available_recipes:
                selected_recipe = random.choice(available_recipes)
                plan[day][meal] = {
                    'name': selected_recipe['name'],
                    'ingredients': selected_recipe['ingredients']
                }
            else:
                plan[day][meal] = {'name': 'No recipe available', 'ingredients': []}
    return plan

print("Meal plan generated successfully.")
meal_plan = generate_meal_plan()
for day, meals in meal_plan.items():
    print(f"\n{day}:")
    for meal, details in meals.items():
        print(f"  {meal}: {details['name']}")
        if details['ingredients']:
            print("    Ingredients:")
            for ingredient in details['ingredients']:
                print(f"      - {ingredient['name']} ({ingredient['amount']} {ingredient['unit']})")
        else:
            print("    No ingredients available.")
