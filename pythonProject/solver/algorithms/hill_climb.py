import time
import random
from typing import Callable, List, Tuple
from solver.problem import SubsetSum


def hill_climb(
    problem: SubsetSum,
    neighborhood: Callable[[List[int]], List[List[int]]],
    time_limit: float = None,
    random_choice: bool = False
) -> Tuple[List[int], int, List[Tuple[float, int]]]:
    """
    Perform hill climbing on the Subset Sum problem.

    Args:
        problem: SubsetSum instance with values and target.
        neighborhood: function to generate neighbors (flip or all).
        time_limit: optional max runtime (seconds).
        random_choice: if True, pick a random improving neighbor; otherwise pick the best.

    Returns:
        best_solution: bit vector of the best subset found.
        best_obj: objective value of best_solution.
        history: list of (elapsed_time, best_obj) on each improvement.
    """
    start_time = time.time()
    # Initialize current and best solutions
    current = problem.random_solution()
    current_obj = problem.objective(current)
    best = current.copy()
    best_obj = current_obj

    history: List[Tuple[float, int]] = []
    history.append((0.0, best_obj))  # record initial state

    while True:
        # Stop if time limit is exceeded
        if time_limit is not None and (time.time() - start_time) > time_limit:
            break

        # Generate neighboring solutions
        raw_neighbors = neighborhood(current)
        if not raw_neighbors:
            break
        # Handle case where single neighbor is returned as list of ints
        if isinstance(raw_neighbors[0], int):
            raw_neighbors = [raw_neighbors]  # type: ignore

        # Evaluate all neighbors and collect those that improve
        improvements: List[Tuple[List[int], int]] = []
        for nbr in raw_neighbors:
            obj = problem.objective(nbr)
            if obj < current_obj:
                improvements.append((nbr, obj))

        # No improvement possible, exit loop
        if not improvements:
            break

        # Select next solution: random or best
        if random_choice:
            next_sol, next_obj = random.choice(improvements)
        else:
            next_sol, next_obj = min(improvements, key=lambda x: x[1])

        current, current_obj = next_sol, next_obj

        # Update best if improved and record time
        if current_obj < best_obj:
            best = current.copy()
            best_obj = current_obj
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))
            if best_obj == 0:
                break

    return best, best_obj, history
