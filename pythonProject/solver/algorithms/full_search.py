import itertools
import math
from typing import Tuple, List

from solver.problem import SubsetSum


def full_search(problem: SubsetSum, time_limit: float = None) -> Tuple[List[int], int]:
    """
    Pełny przegląd przestrzeni rozwiązań: iteruje przez wszystkie 2^n kombinacji.
    Zwraca najlepsze rozwiązanie (wektor bitów) oraz jego wartość funkcji celu.
    time_limit jest opcjonalny, można go wykorzystać do przerywania po określonym czasie.
    """
    best_solution: List[int] = []
    best_obj: int = math.inf

    # Generator kolejnych wektorów 0/1
    for sol in itertools.product([0, 1], repeat=problem.n):
        sol = list(sol)
        obj = problem.objective(sol)
        if obj < best_obj:
            best_obj = obj
            best_solution = sol.copy()
            # Jeśli znalazło się idealne rozwiązanie (0 różnicy), można przerwać
            if best_obj == 0:
                break
    return best_solution, best_obj
