import time
import math
import random
from typing import Callable, List, Tuple
from solver.problem import SubsetSum


def simulated_annealing(
    problem: SubsetSum,
    neighborhood: Callable[[List[int]], List[int]],
    schedule: str = 'exponential',
    time_limit: float = None,
    initial_temp: float = 100.0,
    alpha: float = 0.95,
    min_temp: float = 1e-3
) -> Tuple[List[int], int, List[Tuple[float, int]]]:
    """
    Perform simulated annealing to minimize |sum(selected) - target| for Subset Sum.

    Args:
        problem: SubsetSum instance containing the values array and target sum.
        neighborhood: function generating one neighbor solution from current state.
        schedule: temperature update scheme, either 'exponential' or 'linear'.
        time_limit: optional maximum runtime in seconds before stopping.
        initial_temp: starting temperature for annealing process.
        alpha: cooling factor (multiplier for exponential) or decrement for linear.
        min_temp: threshold temperature to end the annealing loop.

    Returns:
        best_solution: bit list representing the best subset found.
        best_obj: integer objective value |sum(current) - target| of best_solution.
        history: list of (elapsed_time, best_obj) tuples at each improvement.
    """
    start_time = time.time()

    # Initialize with a random starting solution
    current = problem.random_solution()
    current_obj = problem.objective(current)
    best = current.copy()
    best_obj = current_obj
    temp = initial_temp

    # Record improvement history, starting with initial state
    history: List[Tuple[float, int]] = [(0.0, best_obj)]

    # Main annealing loop: continue while temperature remains above minimum
    while temp > min_temp:
        # Check and enforce time limit
        if time_limit is not None and (time.time() - start_time) > time_limit:
            break

        # Generate a new candidate by flipping a bit (or other neighborhood move)
        neighbor = neighborhood(current)
        neighbor_obj = problem.objective(neighbor)

        # Calculate change in objective (energy difference)
        delta = neighbor_obj - current_obj
        # Always accept improvement; accept worse with probability exp(-delta/temp)
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = neighbor
            current_obj = neighbor_obj

            # If this is the best solution so far, record it
            if current_obj < best_obj:
                best = current.copy()
                best_obj = current_obj
                elapsed = time.time() - start_time
                history.append((elapsed, best_obj))

                # Early exit if perfect match found
                if best_obj == 0:
                    break

        # Update the temperature according to the chosen schedule
        if schedule == 'exponential':
            temp *= alpha
        elif schedule == 'linear':
            temp -= alpha
        else:
            temp *= alpha

    return best, best_obj, history
