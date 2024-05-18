import time

import pandas as pd
import concurrent.futures
from tests_knapsack.tests import get_tests as knapsack_tests
from tests_tsp.tests import get_tests as tsp_tests
from tsp import control_loop as control_loop_tsp
from knapsack import control_loop as control_loop_knapsack
from collections import defaultdict

if __name__ == "__main__":
    metrics_knapsack = defaultdict(list)
    test_names_knapsack = []
    for test_name, (capacity, profits, weights, choice, optimal_profit) in knapsack_tests().items():
        test_names_knapsack.append(test_name)
        metrics_knapsack["Capacity"].append(capacity)
        metrics_knapsack["Optimal profit"].append(optimal_profit)
        metrics_knapsack["Optimal choice"].append(str(choice))

        best_profit, best_result_weight, best_result, best_result_time, best_result_init_population_size, best_result_mutation_probability = control_loop_knapsack(
            profits, weights, capacity)
        metrics_knapsack["Genetic Algo Best Profit"].append(best_profit)
        metrics_knapsack["Genetic Algo Total Weight"].append(best_result_weight)
        metrics_knapsack["Genetic Algo Choice"].append(str(best_result))
        metrics_knapsack["Genetic Algo Time"].append(f'{best_result_time:.{2}}')
        metrics_knapsack["Genetic Algo Init Population Size"].append(best_result_init_population_size)
        metrics_knapsack["Genetic Algo Mutation Probability"].append(best_result_mutation_probability)

    df = pd.DataFrame(metrics_knapsack, index=test_names_knapsack)
    print(df.to_markdown())

    metrics_tcp = defaultdict(list)
    test_names_tcp = []
    futures = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for test_name, (adj, opt_solution) in tsp_tests().items():
            test_names_tcp.append(test_name)
            print(f"{test_name=} submit")
            future = executor.submit(control_loop_tsp, adj)
            futures.append(future)

        while any(future.running() for future in futures):
            time.sleep(60)

        for future in futures:
            best_result, best_result_chromosome, best_result_time, best_result_init_population_size, best_result_mutation_probability = future.result()
            metrics_tcp["Genetic Algo Min Path Sum"].append(best_result)
            metrics_tcp["Genetic Algo Min Result Chromosome"].append(str(best_result_chromosome))
            metrics_tcp["Genetic Algo Time"].append(f'{best_result_time:.{2}}')
            metrics_tcp["Genetic Algo Init Population Size"].append(best_result_init_population_size)
            metrics_tcp["Genetic Algo Mutation Probability"].append(best_result_mutation_probability)

    df = pd.DataFrame(metrics_tcp, index=test_names_tcp)
    print(df.to_markdown())
