import random
from typing import List

"""
Moduł zawierający funkcje generujące sąsiedztwo dla problemu Subset Sum.
"""


def flip_neighbor(solution: List[int]) -> List[int]:
    """
    Zwraca nową listę stanów, gdzie losowo odwracamy jeden bit (0->1 lub 1->0).
    """
    n = len(solution)
    idx = random.randrange(n)
    neighbor = solution.copy()
    neighbor[idx] = 1 - neighbor[idx]
    return neighbor


def all_neighbors(solution: List[int]) -> List[List[int]]:
    """
    Zwraca listę wszystkich sąsiedztw powstałych przez odwrócenie każdego bitu po kolei.
    """
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution.copy()
        neighbor[i] = 1 - neighbor[i]
        neighbors.append(neighbor)
    return neighbors
