import random
from typing import List


# Module providing neighborhood generation functions for the Subset Sum problem.

def flip_neighbor(solution: List[int]) -> List[int]:
    """
    Generate a single neighbor by flipping one randomly chosen bit in the solution.

    Parameters:
    - solution: current bit-vector solution

    Returns:
    - A new bit-vector with one bit toggled (0→1 or 1→0)
    """
    n = len(solution)
    idx = random.randrange(n)
    neighbor = solution.copy()
    neighbor[idx] = 1 - neighbor[idx]
    return neighbor


def all_neighbors(solution: List[int]) -> List[List[int]]:
    """
    Generate all neighbors by flipping each bit of the solution one at a time.

    Parameters:
    - solution: current bit-vector solution

    Returns:
    - A list of new bit-vectors, each differing by exactly one bit flip
    """
    neighbors: List[List[int]] = []
    for i in range(len(solution)):
        neighbor = solution.copy()
        neighbor[i] = 1 - neighbor[i]
        neighbors.append(neighbor)
    return neighbors
