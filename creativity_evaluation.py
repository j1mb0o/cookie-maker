import json


def calculate_creativity_score(generated_recipe, original_recipes):

    # Calculate the max Jaccard similarity between the generated recipe and each original recipe
    max_similarity = max(
        len(generated_recipe.intersection(original))
        / len(generated_recipe.union(original))
        for original in original_recipes
    )
    # Calculate creativity as the uniqueness score (higher score means more creative)
    creativity_score = 1 - max_similarity
    return creativity_score * 100  # Convert to percentage


if __name__ == "__main__":

    # Example data
    original_recipes = [
        {"ingredient1", "ingredient2", "ingredient3"},
        {"ingredient2", "ingredient4", "ingredient5"},
        # Add more original recipes as needed
    ]
    generated_recipe = {
        "ingredient1",
        "ingredient5",
        "ingredient6",
    }  # A single generated recipe

    # Calculate creativity score
    creativity_score = calculate_creativity_score(generated_recipe, original_recipes)
    print(
        f"Creativity Score: {creativity_score:.2f}%"
    )  # Output: Creativity Score: 66.67%

    generated_recipe = {
        "spelt flour",
        "baking soda",
        "baking powder",
        "salt",
        "sugar",
        "butter",
        "milk of choice",
        "pure vanilla extract",
        "cream cheese",
        "sugar",
    }

    with open("recipes_expanded.json") as f:
        recipes = json.load(f)

    original_recipes = [
        {ingredient["ingredient"] for ingredient in recipe["ingredients"]}
        for recipe in recipes
    ]

    creativity_score = calculate_creativity_score(generated_recipe, original_recipes)
    print(
        f"Creativity Score: {creativity_score:.2f}%"
    )  # Output: Creativity Score: 66.67%
