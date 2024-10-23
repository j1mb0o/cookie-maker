from langchain_ollama.llms import OllamaLLM
from genetic_algo import generate_recipe
import json
import pprint

def get_promt(rec_items):
    prompt = f"""
    From the folowing recipe give me a creative name for a cookie recipe. The name should be only based on the ingredients. 
    
    {rec_items}

    Return only the name of the recipe, without any additional information.
    """


    return prompt

ollama = OllamaLLM(model="llama3:8b")

with open("recipes_expanded.json") as f:
        recipes = json.load(f)


creative_recipes = []

for _ in range(5):
    temp = {}
    recipe, fitness_value = generate_recipe(recipes)
    recipe_items = [i['ingredient'] for i in recipe]
    for i in recipe:
        print(i['ingredient'])
    print()

    creative_name = ollama.invoke(get_promt(rec_items=recipe_items))
    print(creative_name)

    temp[creative_name] = recipe
    temp['fitness_value'] = fitness_value
    creative_recipes.append(temp)

pprint.pprint(creative_recipes)

with open("creative_recipes.json", "w") as f:
    json.dump(creative_recipes, f, indent=2)