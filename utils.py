import json
from typing import List, Dict
import re

recipes_file_path = './recipes.json'
store_amounts_file_path = './store_amounts.json'


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

def get_ingredient_amounts_with_units(recipes: List[Dict]) -> Dict[str, Dict[str, float]]:
    ingredient_info = {}
    for recipe in recipes:
        for ingredient in recipe['ingredients']:
            name = ingredient['name']
            amount = ingredient['amount']
            unit = ingredient.get('unit', '')
            if name in ingredient_info:
                ingredient_info[name]['amount'] += amount
            else:
                ingredient_info[name] = {'amount': amount, 'unit': unit}
    return ingredient_info

# print("Ingredient amounts with units:")
# ingredient_info = get_ingredient_amounts_with_units(load_recipes(recipes_file_path))
# for ingredient, info in ingredient_info.items():
#     print(f"{ingredient}: {info['amount']} {info['unit']}")

def load_store_amounts(file_path: str) -> Dict[str, float]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    amounts = data.get('amounts', {})
    return {re.sub(r"\(.*?\)", "", k).strip().lower(): v for k, v in amounts.items()}

# store_amounts = load_store_amounts(store_amounts_file_path)
# print("These are the available ingredients in the store:")
# for ingredient, amount in store_amounts.items():
#     print(f"- {ingredient}: {amount} units")


def compute_shopping_list(recipes: List[Dict], store_amounts_path: str) -> Dict[str, Dict]:
    totals = get_ingredient_amounts_with_units(recipes)
    store = load_store_amounts(store_amounts_path)

    shopping = {}
    for raw_name, info in totals.items():
        norm = re.sub(r"\(.*?\)", "", raw_name).strip().lower()
        needed = info.get('amount', 0)
        unit = info.get('unit', '')
        stock = store.get(norm, 0)
        to_buy = max(0, needed - stock)
        shopping[norm] = {
            'needed': needed,
            'unit': unit,
            'stock': stock,
            'to_buy': to_buy,
            'remaining_after_use': stock - needed
        }
    return shopping

# shopping_list = compute_shopping_list(load_recipes(recipes_file_path), store_amounts_file_path)
# for ingredient, info in shopping_list.items():
#     print(f"{ingredient}: need {info['needed']} {info['unit']}")

def compute_leftovers(recipes: List[Dict], store_amounts_path: str, include_negatives: bool = True) -> Dict[str, Dict]:
    totals = get_ingredient_amounts_with_units(recipes)
    totals_norm: Dict[str, Dict] = {}
    for raw_name, info in totals.items():
        norm = re.sub(r"\(.*?\)", "", raw_name).strip().lower()
        totals_norm[norm] = {'needed': info.get('amount', 0), 'unit': info.get('unit', '')}

    store = load_store_amounts(store_amounts_path)

    leftovers: Dict[str, Dict] = {}
    all_keys = set(store.keys()) | set(totals_norm.keys())
    for key in sorted(all_keys):
        stock = store.get(key, 0)
        needed = totals_norm.get(key, {}).get('needed', 0)
        unit = totals_norm.get(key, {}).get('unit', '')
        remaining = stock - needed
        if include_negatives or remaining > 0:
            leftovers[key] = {
                'remaining': remaining,
                'unit': unit,
                'stock': stock,
                'needed': needed
            }
    return leftovers

recipes = load_recipes(recipes_file_path)
leftovers = compute_leftovers(recipes, store_amounts_file_path, include_negatives=False)
for ing, info in leftovers.items():
    print(f"{ing}: remaining {info['remaining']} {info['unit']}")
