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
    def mutation_code():
        pass


if __name__ == "__main__":
    with open("dummy.json") as f:
        recipes = json.load(f)

    # print(population_selection(recipes)[0])
    new_population = population_selection(recipes)
    cross_over = crossover_population(new_population, uniform_crossover)

