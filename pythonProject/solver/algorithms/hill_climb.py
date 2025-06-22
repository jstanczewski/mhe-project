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
    Algorytm wspinaczkowy dla problemu Subset Sum.

    Parametry:
    - problem: instancja SubsetSum
    - neighborhood: funkcja sąsiedztwa (flip_neighbor lub all_neighbors)
    - time_limit: opcjonalne ograniczenie czasu w sekundach
    - random_choice: jeśli True, spośród lepszych sąsiadów wybierany jest losowo;
                     jeśli False, wybierany jest najlepszy sąsiad deterministycznie.

    Zwraca:
    - best_solution: najlepszy znaleziony wektor bitów
    - best_obj: wartość funkcji celu dla best_solution
    - history: lista krotek (czas od startu, best_obj) rejestrująca postęp algorytmu
    """
    start_time = time.time()
    # Start z losowego rozwiązania
    current = problem.random_solution()
    current_obj = problem.objective(current)
    best = current.copy()
    best_obj = current_obj

    history: List[Tuple[float, int]] = []
    # Zapisz stan początkowy
    history.append((0.0, best_obj))

    while True:
        # Check time limit
        if time_limit is not None and time.time() - start_time > time_limit:
            break

        # Generate neighbors
        raw_neighbors = neighborhood(current)
        if not raw_neighbors:
            break
        # Normalize single neighbor
        if isinstance(raw_neighbors[0], int):
            raw_neighbors = [raw_neighbors]  # type: ignore

        # Evaluate neighbors
        improvements: List[Tuple[List[int], int]] = []
        for nbr in raw_neighbors:
            obj = problem.objective(nbr)
            if obj < current_obj:
                improvements.append((nbr, obj))

        if not improvements:
            # No better neighbor found
            break

        # Choose next solution
        # random
        if random_choice:
            next_sol, next_obj = random.choice(improvements)
        # deterministic
        else:
            next_sol, next_obj = min(improvements, key=lambda x: x[1])

        current, current_obj = next_sol, next_obj

        # Update global best and record
        if current_obj < best_obj:
            best = current.copy()
            best_obj = current_obj
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))
            if best_obj == 0:
                break

    return best, best_obj, history
