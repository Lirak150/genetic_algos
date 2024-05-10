import tsplib95
from pathlib import Path

TEST_NAMES = ["a280", "att48", "bays29", "ch150", "fl417", "gr17"]


def get_problem(file_name):
    with file_name.open(mode="r") as file_fd:
        return tsplib95.parse(file_fd.read())


def get_tests():
    current_dir = Path(__file__).parent
    tests = dict()
    for test_name in TEST_NAMES:
        test_file = current_dir / test_name
        tour_file = current_dir / f"{test_name}.tour"
        test_problem = get_problem(test_file)
        opt_solution = None
        if tour_file.exists():
            tour = get_problem(tour_file)
            opt_solution = test_problem.trace_tours(tour.tours)
        tests[test_name] = (test_problem.get_graph(normalize=True).adj, opt_solution[0] if opt_solution else None)
    return tests