import random
from typing import List


class SubsetSum:
    """
    Klasa reprezentująca instancję problemu Subset Sum.
    values: lista liczb całkowitych
    target: wartość celu sumy
    n: liczba elementów
    """
    def __init__(self, values: List[int], target: int):
        self.values = values
        self.target = target
        self.n = len(values)

    @staticmethod
    def from_file(path: str) -> 'SubsetSum':
        """
        Wczytuje instancję z pliku o formacie:
            n T
            a1 a2 ... an
        """
        with open(path, 'r') as f:
            first = f.readline().strip().split()
            if len(first) != 2:
                raise ValueError(f"Niepoprawny format pierwszej linii: {first}")
            n, target = map(int, first)
            values_line = f.readline().strip().split()
            values = list(map(int, values_line))
        if len(values) != n:
            raise ValueError(f"Oczekiwano {n} wartości, ale otrzymano {len(values)}")
        return SubsetSum(values, target)

    def random_solution(self) -> List[int]:
        """
        Generuje losowe rozwiązanie jako wektor 0/1.
        """
        return [random.choice([0, 1]) for _ in range(self.n)]

    def objective(self, solution: List[int]) -> int:
        """
        Funkcja celu: |sum(selected) - target|
        """
        total = sum(val for val, bit in zip(self.values, solution) if bit)
        return abs(total - self.target)
