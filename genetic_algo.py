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
    
    # return random.choices(population, weights=[x["weight"] for x in population], k = 10)
    # population_ = []
    for pop in population:
        pop["weight"] = fitness_function(pop["ingredients"])
        # population_.append(pop)

    population = random.choices(population, weights=[x["weight"] for x in population], k = len(population))

    return population

# crossover


# mutation




if __name__ == "__main__":
    with open("recipes_expanded.json") as f:
        recipes = json.load(f)

    # print(population_selection(recipes)[0])
    new_population = population_selection(recipes)