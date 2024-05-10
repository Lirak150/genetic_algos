import random
import time
import numpy as np

GENERATIONS = 200


def initial_population(vertex_list, population_size):
    population_perms = []
    for _ in range(population_size):
        population_perms.append(np.random.permutation(vertex_list).tolist())

    return population_perms


def chromosome_total_dist(chromosome: list[int], adj):
    fitness_value = 0
    chromosome_len = len(chromosome)
    for ind in range(chromosome_len):
        if ind == chromosome_len - 1:
            fitness_value += adj[chromosome[ind]][chromosome[0]]["weight"]
        else:
            fitness_value += adj[chromosome[ind]][chromosome[ind + 1]]["weight"]
    return fitness_value


def selection(population, adj, k=1):
    fitness_values = [chromosome_total_dist(chromosome=chromosome, adj=adj) for
                      chromosome in population]
    fitness_values_sum = sum(fitness_values)
    fitness_values = [fitness_value / fitness_values_sum for fitness_value in fitness_values]
    parents = random.choices(population, weights=fitness_values, k=k)

    return parents


def cut_crossover(parent_1: list[int], parent_2: list[int], chromosome_len: int):
    cut = random.randint(1, chromosome_len - 1)

    child_1 = parent_1[0:cut]
    child_1 += [city for city in parent_2 if city not in child_1]

    child_2 = parent_2[0:cut]
    child_2 += [city for city in parent_1 if city not in child_2]

    return child_1, child_2


def mutation(child):
    cut = len(child) - 1
    index_1 = random.randint(0, cut)
    index_2 = random.randint(0, cut)

    tmp = child[index_1]
    child[index_1] = child[index_2]
    child[index_2] = tmp
    return child


def get_best(population, adj):
    min_result = float("inf")
    min_idx = 0
    for idx, chromosome in enumerate(population):
        current_dist = chromosome_total_dist(chromosome, adj)
        if current_dist < min_result:
            min_result = current_dist
            min_idx = idx
    return min_result, population[min_idx]


def control_loop(adj):
    population_sizes = [400, 600, 800, 1200, 1400, 2000]
    mutation_probabilities = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3]
    best_result, best_result_chromosome, best_result_init_population_size, best_result_mutation_probability, best_result_time = float(
        "inf"), None, None, None, None
    items = list(adj)
    for population_size in population_sizes:
        for mutation_probability in mutation_probabilities:
            start = time.time()
            population = initial_population(vertex_list=items, population_size=population_size)
            for _ in range(GENERATIONS):
                parent1, parent2 = selection(population, adj=adj, k=2)
                parent1 = list(parent1)
                parent2 = list(parent2)
                child1, child2 = cut_crossover(parent1, parent2, chromosome_len=len(items))

                if random.uniform(0, 1) < mutation_probability:
                    child1 = mutation(child1)
                if random.uniform(0, 1) < mutation_probability:
                    child2 = mutation(child2)

                population.append(child1)
                population.append(child2)
            end = time.time()
            all_time = end - start
            result, chromosome = get_best(population, adj)
            if result < best_result:
                best_result = result
                best_result_chromosome = chromosome
                best_result_init_population_size = population_size
                best_result_mutation_probability = mutation_probability
                best_result_time = all_time
    return best_result, best_result_chromosome, best_result_time, best_result_init_population_size, best_result_mutation_probability
