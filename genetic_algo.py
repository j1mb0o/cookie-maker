import json
import random
from typing import List
import pprint

def fitness_function(ing_list: List[int]) -> float:
    taste_sum = 0
    health_sum = 0

    health_sum = sum([x['health'] for x in ing_list])
    taste_sum = sum([x['taste'] for x in ing_list])
    # we prioritize health over taste
    return 0.7 * health_sum + 0.3 * taste_sum


# selection
def population_selection(population: List[dict]) -> List[dict]:
    weights = [fitness_function(pop) for pop in population]
    population = random.choices(population, weights=[fitness_function(pop) for pop in population], k = len(population))

    return population

# crossover
# One-point crossover function 
def one_point_crossover(parent1, parent2):
    # assert len(parent1) == len(parent2), "Both parents must have the same length"
    offspring1 = {}
    offspring2 = {}

    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)  # Exclude endpoints

    parent1, parent2 = parent1["ingredients"], parent2["ingredients"]

    offspring1["ingredients"] = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2["ingredients"] = parent2[:crossover_point] + parent1[crossover_point:]

    offspring1["name"] = ""
    offspring2["name"] = ""

    return offspring1, offspring2

# Uniform crossover function (from the previous example)
def uniform_crossover(parent1, parent2):
    offspring1 = {}
    offspring2 = {}

    parent1, parent2 = parent1["ingredients"], parent2["ingredients"]

    # Create empty ingredients to fill in the gaps
    empty_ingredients = {"ingredient": None, "health": 0, "taste": 0}

    min_len = min(len(parent1), len(parent2))
    max_len = max(len(parent1), len(parent2))

    if len(parent1) < len(parent2):
        parent1 += [empty_ingredients] * (max_len - min_len)
    elif len(parent2) < len(parent1):
        parent2 += [empty_ingredients] * (max_len - min_len)

    offspring1["name"] = ""
    offspring2["name"] = ""
    offspring1["ingredients"] = []
    offspring2["ingredients"] = []
    
    for gene1, gene2 in zip(parent1, parent2):
        if random.random() > 0.5:
            offspring1["ingredients"].append(gene1)
            offspring2["ingredients"].append(gene2)
        else:
            offspring1["ingredients"].append(gene2)
            offspring2["ingredients"].append(gene1)

    # remove empty ingredients
    offspring1["ingredients"] = [x for x in offspring1["ingredients"] if x["ingredient"] is not None]
    offspring2["ingredients"] = [x for x in offspring2["ingredients"] if x["ingredient"] is not None]


    return offspring1, offspring2

# Function to apply crossover to an entire population
def crossover_population(population, crossover_func):
    new_population = []
    
    # Shuffle population to randomly pair them
    random.shuffle(population)
    
    # Loop through population in pairs (assumes even number of individuals)
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i+1]
        
        # Perform crossover on the pair of parents
        offspring1, offspring2 = crossover_func(parent1, parent2)
        
        # Add the offspring to the new population
        new_population.append(offspring1)
        new_population.append(offspring2)
    
    return new_population


# mutation
def mutate_recipe(recipe):
    # mutation_type = random.randint(0, 3)
    mutation_type = 3
    print("Mutation type:", mutation_type)
    # Mutation: Change ingredient amount
    if mutation_type == 0:
        i = random.randint(0, len(recipe['ingredients']) - 1)
        recipe['ingredients'][i] = recipe['ingredients'][i].copy()
        # print("Old amount:",  recipe['ingredients'][i]['amount'])
        recipe['ingredients'][i]['amount'] = int(recipe['ingredients'][i]['amount'] * random(0.25,2))
        # print("New amount:", max(1, recipe['ingredients'][i]['amount'] + int(recipe['ingredients'][i]['amount'] * 0.15)))
        # print("Ingredient:", recipe['ingredients'][i]['ingredient'])

    # Mutation: Change one ingredient to another
    elif mutation_type == 1:
        j = random.randint(0, len(recipe['ingredients']) - 1)
        recipe['ingredients'][j] = recipe['ingredients'][j].copy()

        # Find a new ingredient that is different from the current one
        current_ingredient = recipe['ingredients'][j]-['ingredient']
        possible_substitutes = [ing for ing in unique_ingredients if ing['ingredient'] != current_ingredient]

        if possible_substitutes:
            new_ingredient = random.choice(possible_substitutes)
            recipe['ingredients'][j]['ingredient'] = new_ingredient['ingredient']

        # print("New ingredient:", recipe['ingredients'][j]['ingredient'])
        # print("Old ingredient:", current_ingredient)


    # Mutation: Addition of an ingredient
    elif mutation_type == 2:
        # new_ingredient = random.choice(unique_ingredients).copy()
        new_ingredient = random.choice(unique_inredients).copy()
        new_ingredient['amount'] = random.randint(1, 5)  # Random amount for the new ingredient
        # recipe['ingredients'].append(new_ingredient)
        # if the new ingredient is already in the recipe, add the amount to the existing ingredient and do not append a new ingredient in the recipe
        if new_ingredient['ingredient'] in [ing['ingredient'] for ing in recipe['ingredients']]:
            for ingredient in recipe['ingredients']:
                if ingredient['ingredient'] == new_ingredient['ingredient']:
                    ingredient['amount'] += new_ingredient['amount']
                    break
        else:
            recipe['ingredients'].append(new_ingredient)
        # print("New ingredient:", new_ingredient['ingredient'])
        

    # Mutation: Deletion of an ingredient
    elif mutation_type == 3:
        if len(recipe['ingredients']) > 1:
            deleted_ing = recipe['ingredients'].pop(random.randint(0, len(recipe['ingredients']) - 1))
        # print("Deleted ingredient:", deleted_ing['ingredient'])
    return recipe



if __name__ == "__main__":
    with open("dummy.json") as f:
        recipes = json.load(f)

    budget = 500
    optimum = 10 # 10 * 0.7 + 10 * 0.3 = 7 + 3 = 10
    mutation_rate = 0.2
    crossover_rate = 0.8
    crossover_func = uniform_crossover

    # from the json we get only the ingredients for each recipe
    population = [recipe["ingredients"] for recipe in recipes]
    while budget >=0:
        # make new population
        new_population = population_selection(population)
        # cossover
        if random.random() < crossover_rate:
            cross_over = crossover_population(new_population, crossover_func)
        # mutation
        if random.random() < mutation_rate:
            for recipe in cross_over:
                mutate_recipe(recipe)
        # evaluation

    # print(population_selection(recipes)[0])

