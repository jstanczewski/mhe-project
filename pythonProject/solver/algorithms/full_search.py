import itertools
import math
import time
from typing import Tuple, List

from solver.problem import SubsetSum


def full_search(
    problem: SubsetSum,
    time_limit: float = None
) -> Tuple[List[int], int, List[Tuple[float, int]]]:
    """
    Perform an exhaustive search over all 2^n subsets for the Subset Sum problem.

    Args:
        problem: SubsetSum instance containing the values list and target sum.
        time_limit: Optional max runtime (in seconds) before early termination.

    Returns:
        best_solution: List[int] bit vector representing the best subset found.
        best_obj: int best objective value |sum(selected) - target|.
        history: List of (elapsed_time, best_obj) tuples at each improvement.
    """
    # Initialize best solution placeholder and improvement history
    best_solution: List[int] = []
    best_obj: int = math.inf
    history: List[Tuple[float, int]] = []

    start_time = time.time()

    # Iterate through every combination of bits of length n
    for bits in itertools.product([0, 1], repeat=problem.n):
        # Stop if the time limit has been exceeded
        if time_limit is not None and (time.time() - start_time) > time_limit:
            break

        # Convert tuple to list and evaluate objective
        candidate = list(bits)
        obj = problem.objective(candidate)

        # Record improvement if candidate is better
        if obj < best_obj:
            best_obj = obj
            best_solution = candidate.copy()
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))

            # Exit early if perfect solution is found
            if best_obj == 0:
                break

    return best_solution, best_obj, history
