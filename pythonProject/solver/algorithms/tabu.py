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
    Algorytm Tabu Search dla problemu Subset Sum.

    Parametry:
    - problem: instancja SubsetSum
    - neighborhood: funkcja generująca listę sąsiadów (all_neighbors)
    - tabu_size: maksymalny rozmiar listy tabu (liczba ostatnich ruchów)
    - time_limit: opcjonalne ograniczenie czasu w sekundach

    Zwraca:
    - best_solution: najlepszy znaleziony wektor bitów
    - best_obj: wartość funkcji celu dla best_solution
    - history: lista krotek (czas od startu, best_obj) rejestrująca postęp algorytmu
    """
    start_time = time.time()
    # Inicjalizacja: losowe rozwiązanie
    current = problem.random_solution()
    current_obj = problem.objective(current)
    best = current.copy()
    best_obj = current_obj

    history: List[Tuple[float, int]] = [(0.0, best_obj)]

    tabu_list: List[int] = []  # przechowuje ostatnie indeksy bitów, które były flipowane

    while True:
        # Check time limit
        if time_limit is not None and time.time() - start_time > time_limit:
            break

        # Generate all neighbors
        neighbors = neighborhood(current)
        if not neighbors:
            break

        candidate = None
        candidate_obj = float('inf')
        candidate_move = None

        # Evaluate each neighbor, avoid tabu moves
        for nbr in neighbors:
            # Determine move index: first index where differs
            move_idx = next(i for i, (b1, b2) in enumerate(zip(current, nbr)) if b1 != b2)
            obj = problem.objective(nbr)
            # Aspiration criterion: jeśli lepszy od globalnie najlepszego, można przyjąć
            if obj < best_obj:
                candidate, candidate_obj, candidate_move = nbr, obj, move_idx
                break
            # Wybieraj najlepszy nie-tabu
            if move_idx not in tabu_list and obj < candidate_obj:
                candidate, candidate_obj, candidate_move = nbr, obj, move_idx

        if candidate is None:
            # Brak możliwych kandydatów
            break

        # Zastosuj ruch
        current = candidate
        current_obj = candidate_obj

        # Aktualizuj tabu_list
        tabu_list.append(candidate_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        # Aktualizuj globalny best i zapis historii
        if current_obj < best_obj:
            best = current.copy()
            best_obj = current_obj
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))
            if best_obj == 0:
                break

    return best, best_obj, history
