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
    # offspring1 = {}
    # offspring2 = {}

    crossover_point = random.randint(
        1, min(len(parent1), len(parent2)) - 1
    )  # Exclude endpoints

    parent1, parent2 = parent1, parent2

    # offspring1["ingredients"] = parent1[:crossover_point] + parent2[crossover_point:]
    # offspring2["ingredients"] = parent2[:crossover_point] + parent1[crossover_point:]
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

    # offspring1["name"] = ""
    # offspring2["name"] = ""

    return offspring1, offspring2


# Uniform crossover function (from the previous example)
def uniform_crossover(parent1, parent2):
    offspring1 = []
    offspring2 = []

    parent1, parent2 = parent1, parent2

    # Create empty ingredients to fill in the gaps
    # empty_ingredients = {"ingredient": None, "health": 0, "taste": 0}

    min_len = min(len(parent1), len(parent2))
    max_len = max(len(parent1), len(parent2))

    # if len(parent1) < len(parent2):
    #     parent1 += [empty_ingredients] * (max_len - min_len)
    # elif len(parent2) < len(parent1):
    #     parent2 += [empty_ingredients] * (max_len - min_len)

    

    for gene1, gene2 in zip(parent1, parent2):
        if random.random() > 0.5:
            offspring1.append(gene1)
            offspring2.append(gene2)
        else:
            offspring1.append(gene2)
            offspring2.append(gene1)

    if len(parent1) > len(parent2):
        offspring1 += parent1[len(parent2):]
        offspring2 += parent1[len(parent2):]
    elif len(parent2) > len(parent1):
        offspring1 += parent2[len(parent1):]
        offspring2 += parent2[len(parent1):]

    # remove empty ingredients
    # offspring1 = [
    #     x for x in offspring1 if x["ingredient"] is not None
    # ]
    # offspring2 = [
    #     x for x in offspring2 if x["ingredient"] is not None
    # ]

    return offspring1, offspring2


# Function to apply crossover to an entire population
def crossover_population(population, crossover_func):
    population_ = []

    # Shuffle population to randomly pair them
    random.shuffle(population)

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
        for ingredient in recipe:
            if random.random() < mutation_rate:
                ingredient["amount"] = (
                    min(round(ingredient["amount"] * random.uniform(0.25, 1.5), 2), 500)
                )

    # Mutation: Change one ingredient to another
    if random.random() < mutation_rate:
        if mutation_type == 1:
            j = random.randint(0, len(recipe) - 1)

            # Find a new ingredient that is different from the current one
            current_ingredient = recipe[j]
            if current_ingredient["units"] == "ml":
                possible_substitutes = [
                    ing for ing in LIQUIDS if ing != current_ingredient["ingredient"]
                ]
            else:
                possible_substitutes = [
                    ing for ing in SOLIDS if ing != current_ingredient["ingredient"]
                ]

            if possible_substitutes:
                new_ingredient_name = random.choice(possible_substitutes)
                new_ingredient_scores = UNIQUE_INGREDIENTS[new_ingredient_name].copy()

                exitst = False
                new_ingredient_name = recipe[0]["ingredient"]
                for ingredient in recipe:
                    if ingredient["ingredient"] == new_ingredient_name:
                        ingredient["amount"] += current_ingredient["amount"]
                        exitst = True
                        break
                if not exitst:
                    recipe[j] = {
                        "ingredient": new_ingredient_name,
                        "amount": (current_ingredient["amount"]
                                   if new_ingredient_name != "egg"
                                   else ceil(current_ingredient["amount"] // 50)),
                        "units": "g" if new_ingredient_name in SOLIDS else "ml",
                        "health": new_ingredient_scores["health"],
                        "taste": new_ingredient_scores["taste"],
                    }

        # Mutation: Addition of an ingredient
        elif mutation_type == 2:

            new_ingredient_name = random.choice(LIQUIDS + SOLIDS)
            new_ingredient_amount = random.randint(
                1, 5
            )
            new_ingredient_scores = UNIQUE_INGREDIENTS[new_ingredient_name].copy()

            ingredient_exists = False
            for ingredient in recipe:
                if ingredient["ingredient"] == new_ingredient_name:
                    ingredient["amount"] += new_ingredient_amount
                    ingredient_exists = True
                    break
            if not ingredient_exists:
                recipe.append(
                    {
                        "ingredient": new_ingredient_name,
                        "amount": round(new_ingredient_amount,2),
                        "units": "g" if new_ingredient_name in SOLIDS else "ml",
                        "health": new_ingredient_scores["health"],
                        "taste": new_ingredient_scores["taste"],
                    }
                )

        # Mutation: Deletion of an ingredient
        elif mutation_type == 3:
            if len(recipe) > 1:
                recipe.pop(
                    random.randint(0, len(recipe) - 1)
                )

    for ingredient in recipe:
        if ingredient["amount"] > 500:
            ingredient["amount"] = 500

    return recipe


def generate_recipe(recipe):
    budget = 5000
    global_optimum = 10  # 10 * 0.7 + 10 * 0.3 = 7 + 3 = 10
    optimum = 0
    mutation_rate = 0.3 # change back to 0.2 after testing
    crossover_rate = 0.8
    # crossover_func = uniform_crossover
    best_recipe = None

    pbar = tqdm(total=5000)

    # from the json we get only the ingredients for each recipe
    population = [recipe["ingredients"] for recipe in recipes]
    # print(type(population))
    while budget >= 0 and optimum < global_optimum:
        if budget % 10 == 0:
            pbar.update(10)

        population = population_selection(population)
        # cossover
        if random.random() < crossover_rate:
            crossover_func = random.choice([one_point_crossover, uniform_crossover])
            population = crossover_population(population, crossover_func=crossover_func)
        # mutation
        new_population = []
        for recipe in population:
            mut_type = random.randint(0, 4)
            new_population.append(mutate_recipe(recipe, mutation_type=mut_type, mutation_rate=mutation_rate))
        # evaluation
        clean_recipes = [clean_recipe(recipe) for recipe in new_population]
        for recipe in clean_recipes:
            fitness_ = fitness_function(recipe)
            if fitness_ > optimum:
                optimum = fitness_
                best_recipe = recipe
        budget -= 1
        # population = [recipe["ingredients"] for recipe in new_population]
        population = new_population.copy()
        new_population.clear()
    # print(best_recipe)
    pprint.pprint(best_recipe)
    print(f"Optimum: {optimum}")
    print(len(best_recipe))


def clean_recipe(recipe):
    unique_ingredients = {}
    for ingredient in recipe:
        name = ingredient["ingredient"]
        if name in unique_ingredients:
            unique_ingredients[name]["amount"] += ingredient["amount"]

        else:
            unique_ingredients[name] = ingredient

    final_ingrediens = []
    for ingredient_name, ingredient_stats in zip(unique_ingredients.keys(), unique_ingredients.values()):
        final_ingrediens.append({
            "ingredient": ingredient_name,
            "amount": min(round(ingredient_stats["amount"], 2), 2),
            "units": ingredient_stats["units"],
            "health": ingredient_stats["health"],
            "taste": ingredient_stats["taste"]
        })
    return final_ingrediens

if __name__ == "__main__":
    with open("recipes_expanded.json") as f:
        recipes = json.load(f)
    # test_recipe = [{'amount': 500,
    #         'health': 8,
    #         'ingredient': 'cocoa powder',
    #         'taste': 8,
    #         'units': 'g'},
    #         {'amount': 240.0,
    #         'health': 9,
    #         'ingredient': 'almond flour',
    #         'taste': 7,
    #         'units': 'g'},
    #         {'amount': 80.0, 'health': 6, 'ingredient': 'honey', 'taste': 8, 'units': 'g'},
    #         {'amount': 10.0,
    #         'health': 7,
    #         'ingredient': 'lemon juice',
    #         'taste': 6,
    #         'units': 'g'},
    #         {'amount': 60.0,
    #         'health': 8,
    #         'ingredient': 'cocoa powder',
    #         'taste': 8,
    #         'units': 'g'}]
    # clean_recipe(recipe=test_recipe)

    generate_recipe(recipes)