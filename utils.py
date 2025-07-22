import json
from typing import List, Dict

recipes_file_path = './recipes.json'

def load_recipes(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        recipes = json.load(file)
    return recipes['recipes']

# print("Recipes loaded successfully.")
# print("These are the recipes available in the system:")
# for recipe in load_recipes(recipes_file_path):
#     print(f"- {recipe['name']}")

def filter_recipes_by_type(recipes: List[Dict], meal_type: str) -> List[Dict]:
    return [recipe for recipe in recipes if recipe['type'].lower() == meal_type.lower()]

# print("\n")
# print("Filtered recipes by type:")
# print("Breakfast recipes:")
# for recipe in filter_recipes_by_type(load_recipes(recipes_file_path), 'Breakfast'):
#     print(f"- {recipe['name']}")
# print("\nLunch recipes:")
# for recipe in filter_recipes_by_type(load_recipes(recipes_file_path), 'Lunch'):
#     print(f"- {recipe['name']}")
# print("\nDinner recipes:")
# for recipe in filter_recipes_by_type(load_recipes(recipes_file_path), 'Dinner'):
#     print(f"- {recipe['name']}")
