import time
from typing import Callable, List, Tuple
from solver.problem import SubsetSum


def tabu_search(
    problem: SubsetSum,
    neighborhood: Callable[[List[int]], List[List[int]]],
    tabu_size: int,
    time_limit: float = None
) -> Tuple[List[int], int, List[Tuple[float, int]]]:
    """
    Tabu Search for the Subset Sum problem.

    Parameters:
    - problem: an instance of SubsetSum
    - neighborhood: function that generates a list of neighbors (all_neighbors)
    - tabu_size: maximum length of the tabu list (number of recent moves to forbid)
    - time_limit: optional time limit in seconds

    Returns:
    - best_solution: the best bit-vector found
    - best_obj: the objective value of best_solution
    - history: list of (elapsed_time, best_obj) tuples tracking improvements
    """
    start_time = time.time()

    # Initialize with a random solution
    current = problem.random_solution()
    current_obj = problem.objective(current)
    best = current.copy()
    best_obj = current_obj

    # Record the initial state
    history: List[Tuple[float, int]] = [(0.0, best_obj)]

    # Tabu list stores the indices of bits that were last flipped
    tabu_list: List[int] = []

    while True:
        # Stop if time limit exceeded
        if time_limit is not None and (time.time() - start_time) > time_limit:
            break

        # Generate all neighbors of the current solution
        neighbors = neighborhood(current)
        if not neighbors:
            break

        candidate = None
        candidate_obj = float('inf')
        candidate_move = None

        # Evaluate each neighbor, respecting the tabu list and aspiration criteria
        for nbr in neighbors:
            # Identify which bit was flipped to generate this neighbor
            move_idx = next(i for i, (b1, b2) in enumerate(zip(current, nbr)) if b1 != b2)
            obj = problem.objective(nbr)

            # Aspiration: accept if it's better than the global best
            if obj < best_obj:
                candidate, candidate_obj, candidate_move = nbr, obj, move_idx
                break

            # Otherwise, consider it only if move is not tabu and it's the best so far
            if move_idx not in tabu_list and obj < candidate_obj:
                candidate, candidate_obj, candidate_move = nbr, obj, move_idx

        # If no valid candidate found, terminate
        if candidate is None:
            break

        # Apply the chosen move
        current = candidate
        current_obj = candidate_obj

        # Update tabu list (FIFO)
        tabu_list.append(candidate_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        # Update global best if improved
        if current_obj < best_obj:
            best = current.copy()
            best_obj = current_obj
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))
            # Stop early if perfect solution found
            if best_obj == 0:
                break

    return best, best_obj, history
