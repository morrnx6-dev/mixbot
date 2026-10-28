import json
from pathlib import Path

# Load Cocktail Metadata
def load_cocktail_metadata():
    try:
        with open(Path("data/cocktails.json"), "r") as cocktail_file:
            data = json.load(cocktail_file)
            print("Cocktail metadata loaded successfully.")
            print(f"Number of cocktails loaded: {len(data)}")
            print(f"Sample cocktail data: {data[:1]}")  # Print a sample cocktail
            return data
    except Exception as e:
        print(f"Error loading cocktail metadata: {e}")
        return []

# Load Recipes
def load_cocktail_recipes():
    try:
        with open(Path("data/cocktail_recipes.json"), "r") as recipes_file:
            data = json.load(recipes_file)
            print("Cocktail recipes loaded successfully.")
            print(f"Number of recipes loaded: {len(data)}")
            print(f"Sample recipe data: {list(data.items())[:1]}")  # Print a sample recipe
            return data
    except Exception as e:
        print(f"Error loading cocktail recipes: {e}")
        return {}

# Define Variables from Functions
cocktails = load_cocktail_metadata()
recipes = load_cocktail_recipes()

# For matching cocktail criteria in JSON search, append cocktails to Array
def get_matching_cocktails(user_selected_spirits, user_selected_liqueur, user_selected_ingredients, mood, taste, drink_type, category_filter=None):
    matches = []
    print("Starting cocktail matching process...")
    for cocktail in cocktails:
        print(f"Checking cocktail: {cocktail['name']}")

        # Category Filter
        if category_filter and cocktail.get("category") != category_filter:
            continue

        # Updated the matching logic for spirits/liqueur
        if not cocktail["spirits"]:
            spirits_match = True
        elif len(cocktail["spirits"]) >= 2:
            print("Cocktail has more than or equal to 2 spirits")
            spirits_match = all(spirit in user_selected_spirits for spirit in cocktail["spirits"])
        else:
            spirits_match = any(spirit in cocktail["spirits"] for spirit in user_selected_spirits)

        
        if not cocktail["liqueur"]:
            liqueur_match = True
        elif len(cocktail["liqueur"]) >= 2:
           print("Cocktail has more than or equal to 2 liquer")
           liqueur_match = all(liqueur in user_selected_liqueur for liqueur in cocktail["liqueur"])
        else:
            liqueur_match = any(liqueur in cocktail["liqueur"] for liqueur in user_selected_liqueur)
        
        # Updated logic to match at least 2 ingredients
        # Accomodates for scenarios as Ice is ingredient, and will always match each cocktail
        # Ingredient matching logic (with Egg White special case)
        if "Egg White" in cocktail["ingredients"]:
            ingredients_match = "Egg White" in user_selected_ingredients
        else:
            matching_ingredients_count = sum(
                ingredient in cocktail["ingredients"] for ingredient in user_selected_ingredients
            )
            ingredients_match = matching_ingredients_count >= 2

        mood_match = any(mood in cocktail["moods"] for mood in mood)
        taste_match = any(taste in cocktail["tastes"] for taste in taste)
        type_match = drink_type in cocktail["type"]

        # Consider a cocktail a match if all the selected criteria are true
        if spirits_match and liqueur_match and ingredients_match and mood_match and taste_match and type_match:
            print(f"Cocktail '{cocktail['name']}' matches one or more criteria.")
            matches.append(cocktail)
        else:
            print(f"Cocktail '{cocktail['name']}' does not match any criteria.")
    return matches

# For matching cocktail name, provide the recipe information
def get_matching_cocktail_recipe(cocktail_name):
    return recipes.get(cocktail_name)
