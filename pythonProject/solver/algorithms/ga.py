import time
import random
from typing import List, Tuple
from solver.problem import SubsetSum
from solver.neighborhood import flip_neighbor, all_neighbors


def genetic_algorithm(
    problem: SubsetSum,
    pop_size: int = 100,
    crossover: str = 'one_point',
    mutation: str = 'flip',
    time_limit: float = None
) -> Tuple[List[int], int, List[Tuple[float, int]]]:
    """
    Prosty algorytm genetyczny dla problemu Subset Sum z logowaniem postępu.

    Parametry:
    - problem: instancja SubsetSum
    - pop_size: rozmiar populacji
    - crossover: 'one_point' lub 'uniform'
    - mutation: 'flip' lub 'swap'
    - time_limit: limit czasu w sekundach

    Zwraca:
    - best_solution: najlepszy znaleziony wektor bitów
    - best_obj: wartość funkcji celu dla best_solution
    - history: lista krotek (czas od startu, best_obj) rejestrująca postęp
    """
    start_time = time.time()
    # Inicjalizuj populację losowymi rozwiązaniami
    population: List[List[int]] = [problem.random_solution() for _ in range(pop_size)]
    fitness = [problem.objective(sol) for sol in population]
    best_sol = population[fitness.index(min(fitness))].copy()
    best_obj = min(fitness)

    history: List[Tuple[float, int]] = []
    history.append((0.0, best_obj))

    # Helper funkcje
    def crossover_op(parent1: List[int], parent2: List[int]) -> List[int]:
        n = problem.n
        if crossover == 'one_point':
            point = random.randrange(1, n)
            return parent1[:point] + parent2[point:]
        elif crossover == 'uniform':
            return [parent1[i] if random.random() < 0.5 else parent2[i] for i in range(n)]
        else:
            return parent1.copy()

    def mutate(sol: List[int]) -> List[int]:
        n = problem.n
        child = sol.copy()
        if mutation == 'flip':
            idx = random.randrange(n)
            child[idx] = 1 - child[idx]
        elif mutation == 'swap':
            i, j = random.sample(range(n), 2)
            child[i], child[j] = child[j], child[i]
        return child

    # Główna pętla (generacyjna)
    while True:
        if time_limit is not None and time.time() - start_time > time_limit:
            break

        # Selekcja rodziców (turniej 2)
        def select_parent():
            i, j = random.sample(range(pop_size), 2)
            return population[i] if fitness[i] < fitness[j] else population[j]

        parent1 = select_parent()
        parent2 = select_parent()

        # Krzyżowanie i mutacja
        child = crossover_op(parent1, parent2)
        child = mutate(child)
        obj = problem.objective(child)

        # Dodaj dziecko, usuń najgorszego
        population.append(child)
        fitness.append(obj)
        worst_idx = fitness.index(max(fitness))
        population.pop(worst_idx)
        fitness.pop(worst_idx)

        # Aktualizuj najlepsze
        if obj < best_obj:
            best_obj = obj
            best_sol = child.copy()
            elapsed = time.time() - start_time
            history.append((elapsed, best_obj))
            if best_obj == 0:
                break

    return best_sol, best_obj, history