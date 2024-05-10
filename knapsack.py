import random
import time

GENERATIONS = 5


def init_population(population_size: int, items_len: int):
    population = []
    genes = [0, 1]
    for _ in range(population_size):
        population.append([random.choice(genes) for _ in range(items_len)])
    return population


def calculate_fitness(chromosome: list[int],
                      profits: list[int],
                      weights: list[int],
                      capacity: int):
    total_weight = 0
    total_profit = 0
    for ind, choice in enumerate(chromosome):
        total_weight += weights[ind] * choice
        total_profit += profits[ind] * choice
    return 0 if total_weight > capacity else total_profit


def select_chromosomes(population: list[list[int]],
                       profits: list[int],
                       weights: list[int],
                       capacity: int):
    fitness_values = [calculate_fitness(chromosome=chromosome, weights=weights, profits=profits, capacity=capacity) for
                      chromosome in population]
    fitness_values_sum = sum(fitness_values)
    if not fitness_values_sum:
        return None
    fitness_values = [fitness_value / fitness_values_sum for fitness_value in fitness_values]

    parents = random.choices(population, weights=fitness_values, k=2)

    return parents


def one_point_crossover(parent1: list[int], parent2: list[int], items_len: int):
    crossover_point = random.randint(0, items_len - 1)
    child1 = parent1[0:crossover_point] + parent2[crossover_point:]
    child2 = parent2[0:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(chromosome: list[int]):
    mutation_point = random.randint(0, len(chromosome) - 1)
    if chromosome[mutation_point] == 0:
        chromosome[mutation_point] = 1
    else:
        chromosome[mutation_point] = 0
    return chromosome


def get_best(population: list[list[int]],
             profits: list[int],
             weights: list[int],
             capacity: int
             ):
    fitness_values = [calculate_fitness(chromosome=chromosome, weights=weights, profits=profits, capacity=capacity) for
                      chromosome in population]

    max_value = max(fitness_values)
    max_index = fitness_values.index(max_value)
    return population[max_index]


def control_loop(profits: list[int],
                 weights: list[int],
                 capacity: int):
    init_population_sizes = [10, 20, 30, 40, 50]
    mutation_probabilities = [0.001, 0.01, 0.05, 0.1]
    best_profit, best_result, best_result_weight, best_result_init_population_size, best_result_mutation_probability, best_result_time = -1, None, None, None, None, None
    items_len = len(weights)
    for init_population_size in init_population_sizes:
        for mutation_probability in mutation_probabilities:
            start = time.time()
            population = init_population(items_len=items_len, population_size=init_population_size)
            for _ in range(GENERATIONS):
                result = select_chromosomes(population, profits=profits, weights=weights, capacity=capacity)
                if result is None:
                    population = init_population(items_len=items_len, population_size=init_population_size)
                    continue
                else:
                    parent1, parent2 = result
                child1, child2 = one_point_crossover(parent1, parent2, items_len=items_len)
                if random.uniform(0, 1) < mutation_probability:
                    child1 = mutate(child1)
                if random.uniform(0, 1) < mutation_probability:
                    child2 = mutate(child2)

                population.append(child1)
                population.append(child2)
            end = time.time()
            all_time = end - start
            best = get_best(population, profits=profits, weights=weights, capacity=capacity)
            total_weight = 0
            total_profit = 0
            for ind, choice in enumerate(best):
                total_weight += weights[ind] * choice
                total_profit += profits[ind] * choice
            if total_profit > best_profit:
                best_profit = total_profit
                best_result = best
                best_result_weight = total_weight
                best_result_init_population_size = init_population_size
                best_result_mutation_probability = mutation_probability
                best_result_time = all_time
    return best_profit, best_result_weight, best_result, best_result_time, best_result_init_population_size, best_result_mutation_probability
