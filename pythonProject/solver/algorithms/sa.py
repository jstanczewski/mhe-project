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
    Algorytm symulowanego wyżarzania dla problemu Subset Sum.

    Parametry:
    - problem: instancja SubsetSum
    - neighborhood: funkcja generująca losowego sąsiada (flip_neighbor)
    - schedule: schemat obniżania temperatury ('exponential' lub 'linear')
    - initial_temp: początkowa temperatura
    - alpha: współczynnik chłodzenia (dla exponential)
    - min_temp: minimalna temperatura, po której kończymy
    - time_limit: opcjonalne ograniczenie czasu w sekundach

    Zwraca:
    - best_solution: najlepszy znaleziony wektor bitów
    - best_obj: wartość funkcji celu dla best_solution
    - history: lista krotek (czas, best_obj) rejestrująca postęp algorytmu
    """
    start_time = time.time()
    # Start z losowego rozwiązania
    current = problem.random_solution()
    current_obj = problem.objective(current)
    best = current.copy()
    best_obj = current_obj
    temp = initial_temp

    history: List[Tuple[float, int]] = [(0.0, best_obj)]
    # Zapisz stan początkowy

    iteration = 0
    while temp > min_temp:
        if time_limit is not None and time.time() - start_time > time_limit:
            break

        # Generate neighbor solution
        neighbor = neighborhood(current)
        neighbor_obj = problem.objective(neighbor)

        # Accept if better or by probability
        delta = neighbor_obj - current_obj
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = neighbor
            current_obj = neighbor_obj
            # Update best
            if current_obj < best_obj:
                best = current.copy()
                best_obj = current_obj
                # Record improvement
                elapsed = time.time() - start_time
                history.append((elapsed, best_obj))
                if best_obj == 0:
                    break

        # Update temperature
        if schedule == 'exponential':
            temp *= alpha
        elif schedule == 'linear':
            temp -= alpha
        else:
            temp *= alpha

        iteration += 1

    return best, best_obj, history
