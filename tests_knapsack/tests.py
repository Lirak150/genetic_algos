from pathlib import Path
from time import time

TEST_NAMES = ["p01", "p02", "p03", "p04", "p05", "p06", "p07"]


def get_file_content(file_name):
    with file_name.open(mode="r") as file_fd:
        return file_fd.read().strip()


def get_tests() -> dict[str, tuple[int, list[int], list[int], list[int], int]]:
    current_dir = Path(__file__).parent
    tests = dict()
    for test in TEST_NAMES:
        test_dir = current_dir / test
        weights = [int(item) for item in get_file_content(test_dir / f"{test}_w.txt").split()]
        profits = [int(item) for item in get_file_content(test_dir / f"{test}_p.txt").split()]
        capacity = int(get_file_content(test_dir / f"{test}_c.txt").split()[0])
        choice = [int(item) for item in get_file_content(test_dir / f"{test}_s.txt").split()]
        optimal_profit = sum(single_choice * single_profit for single_choice, single_profit in zip(choice, profits))
        tests[test] = capacity, profits, weights, choice, optimal_profit
    return tests


def timing(times, func, *args, **kwargs):
    experiments = []
    for _ in range(times):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        experiments.append(end - start)
    return sum(experiments) / len(experiments), result
