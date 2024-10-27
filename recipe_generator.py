from langchain_ollama.llms import OllamaLLM
from genetic_algo import generate_recipe
import json
import pprint
from creativity_evaluation import calculate_creativity_score


def get_promt(rec_items):
    prompt = f"""
    From the folowing recipe give me a very creative name for a cookie recipe. The name should be only based on the ingredients. 
    
    {rec_items}

    Return only the name of the recipe, without any additional information.
    """

    return prompt


ollama = OllamaLLM(model="llama3:8b")

with open("recipes_expanded.json") as f:
    recipes = json.load(f)


creative_recipes = []

original_recipes = [
    {ingredient["ingredient"] for ingredient in recipe["ingredients"]}
    for recipe in recipes
]

for _ in range(4):
    temp = {}
    recipe, fitness_value = generate_recipe(recipes)
    if len(recipe) < 3:
        continue
    recipe_items = [i["ingredient"] for i in recipe]
    # for i in recipe:
    #     print(i["ingredient"])
    # print()

    creative_name = ollama.invoke(get_promt(rec_items=recipe_items))

    temp["creative_name"] = creative_name
    temp["fitness_value"] = fitness_value
    temp["recipe"] = recipe
    
    recipe_ingredients = {i["ingredient"] for i in recipe}
    creavive_score = calculate_creativity_score(
        original_recipes=original_recipes, generated_recipe=recipe_ingredients
    )
    temp["creativity_score"] = creavive_score
    creative_recipes.append(temp)

    print(f"Name: {creative_name:>20} \t Creative Score: {creavive_score:.2f}%")
    # print(f"Ingedients: {('\n'.join(list(recipe_ingredients)):>20)}")
    joined_ingredients = '\n\t\t'.join(recipe_ingredients)

    print(f"Ingredients:\t{joined_ingredients:>20}")



# pprint.pprint(creative_recipes)

with open("creative_recipes.json", "w") as f:
    json.dump(creative_recipes, f, indent=2)
