import random
from typing import List


class SubsetSum:
    """
    Represents a Subset Sum problem instance.

    Attributes:
    - values: list of integers (the input numbers)
    - target: integer (the desired sum)
    - n: number of elements in 'values'
    """
    def __init__(self, values: List[int], target: int):
        self.values = values
        self.target = target
        self.n = len(values)

    @staticmethod
    def from_file(path: str) -> 'SubsetSum':
        """
        Load a Subset Sum instance from a file.

        Expected file format:
            n target
            a1 a2 ... an

        Where 'n' is the number of values and 'target' is the desired sum.
        """
        with open(path, 'r') as f:
            # Read and parse the first line (n and target)
            first_line = f.readline().strip().split()
            if len(first_line) != 2:
                raise ValueError(f"Invalid header line: {first_line}")
            n, target = map(int, first_line)

            # Read and parse the list of values
            values_tokens = f.readline().strip().split()
            values = list(map(int, values_tokens))

        # Validate that we have exactly n values
        if len(values) != n:
            raise ValueError(f"Expected {n} values, but got {len(values)}")

        return SubsetSum(values, target)

    def random_solution(self) -> List[int]:
        """
        Generate a random solution represented as a bit-vector of length n.

        Each entry is 0 (exclude that value) or 1 (include that value).
        """
        return [random.choice([0, 1]) for _ in range(self.n)]

    def objective(self, solution: List[int]) -> int:
        """
        Compute the objective value for a given solution.

        Returns the absolute difference between the sum of selected values
        and the target.
        """
        total = sum(val for val, bit in zip(self.values, solution) if bit)
        return abs(total - self.target)
