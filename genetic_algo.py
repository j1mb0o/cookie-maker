import json
import random
from typing import List
import pprint
from consts import UNIQUE_INGREDIENTS, LIQUIDS, SOLIDS
from math import ceil
from tqdm import tqdm
import time


def fitness_function(ing_list: List[int]) -> float:
    taste_sum = 0
    health_sum = 0

    health_sum = sum([x["health"] for x in ing_list])
    taste_sum = sum([x["taste"] for x in ing_list])
    # we prioritize health over taste
    return (0.7 * health_sum + 0.3 * taste_sum) / len(ing_list)


# selection
def population_selection(population: List[dict]) -> List[dict]:
    weights = [fitness_function(pop) for pop in population]
    population = random.choices(
        population,
        weights=[fitness_function(pop) for pop in population],
        k=len(population),
    )

    return population


# crossover
# One-point crossover function
def one_point_crossover(parent1, parent2):
    # assert len(parent1) == len(parent2), "Both parents must have the same length"
    offspring1 = {}
    offspring2 = {}

    crossover_point = random.randint(
        1, min(len(parent1), len(parent2)) - 1
    )  # Exclude endpoints

    parent1, parent2 = parent1, parent2

    offspring1["ingredients"] = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2["ingredients"] = parent2[:crossover_point] + parent1[crossover_point:]

    offspring1["name"] = ""
    offspring2["name"] = ""

    return offspring1, offspring2


# Uniform crossover function (from the previous example)
def uniform_crossover(parent1, parent2):
    offspring1 = {}
    offspring2 = {}

    parent1, parent2 = parent1, parent2

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
    offspring1["ingredients"] = [
        x for x in offspring1["ingredients"] if x["ingredient"] is not None
    ]
    offspring2["ingredients"] = [
        x for x in offspring2["ingredients"] if x["ingredient"] is not None
    ]

    return offspring1, offspring2


# Function to apply crossover to an entire population
def crossover_population(population, crossover_func):
    population_ = []

    # Shuffle population to randomly pair them
    random.shuffle(population)

    # Loop through population in pairs (assumes even number of individuals)
    # for i in range(0, len(population), 2):
    # parent1 = population[i]
    # parent2 = population[i+1]
    while len(population_) < len(population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        # Perform crossover on the pair of parents
        offspring1, offspring2 = crossover_func(parent1, parent2)

        # Add the offspring to the new population
        population_.append(offspring1)
        population_.append(offspring2)

    return population_


# mutation
def mutate_recipe(recipe, mutation_type=0, mutation_rate=0.2):
    # Mutation: Change ingredient amount
    if mutation_type == 0:
        for ingredient in recipe["ingredients"]:
            if random.random() < mutation_rate:
                ingredient["amount"] = (
                    round(ingredient["amount"] * random.uniform(0.25, 2), 2)
                )

    # Mutation: Change one ingredient to another
    if random.random() < mutation_rate:
        if mutation_type == 1:
            j = random.randint(0, len(recipe["ingredients"]) - 1)

            # Find a new ingredient that is different from the current one
            current_ingredient = recipe["ingredients"][j]
            if current_ingredient["units"] == "ml":
                possible_substitutes = [
                    ing for ing in LIQUIDS if ing != current_ingredient["ingredient"]
                ]
            else:
                possible_substitutes = [
                    ing for ing in SOLIDS if ing != current_ingredient["ingredient"]
                ]
            # possible_substitutes = [ing for ing in UNIQUE_INGREDIENTS.keys() if ing != current_ingredient]

            if possible_substitutes:
                new_ingredient_name = random.choice(possible_substitutes)
                # new_ingredient_name = 'egg'
                new_ingredient_scores = UNIQUE_INGREDIENTS[new_ingredient_name].copy()
                new_ingredient_amount = (
                    current_ingredient["amount"]
                    if new_ingredient_name != "egg"
                    else ceil(current_ingredient["amount"] // 50)
                )  # a medium egg is around 50g
                # recipe["ingredients"][j]["ingredient"] = {
                recipe["ingredients"][j] = {
                    "ingredient": new_ingredient_name,
                    "amount": new_ingredient_amount,
                    "units": "g" if new_ingredient_name in SOLIDS else "ml",
                    "health": new_ingredient_scores["health"],
                    "taste": new_ingredient_scores["taste"],
                }

        # Mutation: Addition of an ingredient
        elif mutation_type == 2:

            new_ingredient_name = random.choice(LIQUIDS + SOLIDS)
            # new_ingredient_name = recipe["ingredients"][0]["ingredient"]
            new_ingredient_amount = random.randint(
                1, 5
            )  # Random amount for the new ingredient
            new_ingredient_scores = UNIQUE_INGREDIENTS[new_ingredient_name].copy()
            # new_ingredient_scores = {
            #     "health": recipe["ingredients"][0]["health"],
            #     "taste": recipe["ingredients"][0]["taste"],
            # }

            ingredient_exists = False
            for ingredient in recipe["ingredients"]:
                if ingredient["ingredient"] == new_ingredient_name:
                    ingredient["amount"] += new_ingredient_amount
                    ingredient_exists = True
                    break
            if not ingredient_exists:
                recipe["ingredients"].append(
                    {
                        "ingredient": new_ingredient_name,
                        "amount": new_ingredient_amount,
                        "units": "g" if new_ingredient_name in SOLIDS else "ml",
                        "health": new_ingredient_scores["health"],
                        "taste": new_ingredient_scores["taste"],
                    }
                )

        # Mutation: Deletion of an ingredient
        elif mutation_type == 3:
            if len(recipe["ingredients"]) > 1:
                recipe["ingredients"].pop(
                    random.randint(0, len(recipe["ingredients"]) - 1)
                )

    return recipe


if __name__ == "__main__":
    with open("recipes_expanded.json") as f:
        recipes = json.load(f)

    budget = 5000
    global_optimum = 10  # 10 * 0.7 + 10 * 0.3 = 7 + 3 = 10
    optimum = 0
    mutation_rate = 0.5  # change back to 0.2 after testing
    crossover_rate = 1
    crossover_func = one_point_crossover
    best_recipe = None

    pbar = tqdm(total=5000)

    # from the json we get only the ingredients for each recipe
    population = [recipe["ingredients"] for recipe in recipes]
    print(type(population))
    while budget >= 0 and optimum < global_optimum:
        if budget % 10 == 0:
            pbar.update(10)

        population = population_selection(population)
        # cossover
        if random.random() < crossover_rate:
            population = crossover_population(population, crossover_func)
        # mutation
        new_population = []
        for recipe in population:
            mut_type = random.randint(0, 4)
            new_population.append(mutate_recipe(recipe, mutation_type=2, mutation_rate=mutation_rate))
        # evaluation
        for recipe in new_population:
            fitness_ = fitness_function(recipe["ingredients"])
            if fitness_ > optimum:
                optimum = fitness_
                best_recipe = recipe
        budget -= 1
        population = [recipe["ingredients"] for recipe in new_population]
        new_population.clear()
    # print(best_recipe)
    pprint.pprint(best_recipe)
    print(f"Optimum: {optimum}")
