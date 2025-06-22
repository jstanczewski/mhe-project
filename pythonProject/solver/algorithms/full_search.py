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
    Pełny przegląd przestrzeni rozwiązań: iteruje przez wszystkie 2^n kombinacji.
    Zwraca najlepsze rozwiązanie (wektor bitów), jego wartość funkcji celu
    oraz historię postępu w postaci listy (czas_od_startu, best_obj).
    time_limit jest opcjonalny, można go wykorzystać do przerywania po określonym czasie.
    """
    best_solution: List[int] = []
    best_obj: int = math.inf
    history: List[Tuple[float, int]] = []

    start_time = time.time()

    # Generator kolejnych rozwiązań
    for sol in itertools.product([0, 1], repeat=problem.n):
        # Sprawdzenie limitu czasu
        if time_limit is not None and (time.time() - start_time) > time_limit:
            break

        sol_list = list(sol)
        obj = problem.objective(sol_list)

        # Pierwsza poprawa lub lepsze rozwiązanie
        if obj < best_obj:
            best_obj = obj
            best_solution = sol_list.copy()
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))

            # Jeśli idealne rozwiązanie, kończymy
            if best_obj == 0:
                break

    return best_solution, best_obj, history
