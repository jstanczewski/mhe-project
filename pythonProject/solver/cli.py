import argparse
import sys
import random
import time
import csv
from pathlib import Path

from solver.problem import SubsetSum
from solver.neighborhood import flip_neighbor, all_neighbors
from solver.algorithms.full_search import full_search
from solver.algorithms.ga import genetic_algorithm
from solver.algorithms.sa import simulated_annealing
from solver.algorithms.tabu import tabu_search
from solver.algorithms.hill_climb import hill_climb


def parse_args():
    parser = argparse.ArgumentParser(
        description='Solver for Subset Sum using various metaheuristics.')
    parser.add_argument('--input', '-i', required=True,
                        help='Path to input file')
    parser.add_argument('--target', '-T', type=int,
                        help='Override target value from file')
    parser.add_argument('--algorithm', '-a', required=True,
                        choices=['full', 'hill', 'tabu', 'sa', 'ga'],
                        help='Which algorithm to run')
    parser.add_argument('--neighborhood', '-n', choices=['flip', 'all'], default='flip',
                        help='Type of neighborhood to use')
    parser.add_argument('--time-limit', '-t', type=float,
                        help='Time limit in seconds (optional)')
    parser.add_argument('--seed', '-s', type=int,
                        help='Random seed (optional)')
    # Parametry dla hill_climb
    parser.add_argument('--random-choice', action='store_true',
                        help='Random choice among improving neighbors in hill climbing')
    # Parametr dla tabu_search
    parser.add_argument('--tabu-size', type=int, default=50,
                        help='Tabu list size for tabu search')
    # Parametry dla simulated annealing
    parser.add_argument('--initial-temp', type=float, default=100.0,
                        help='Initial temperature for SA')
    parser.add_argument('--alpha', type=float, default=0.95,
                        help='Cooling rate alpha for SA')
    parser.add_argument('--min-temp', type=float, default=1e-3,
                        help='Minimum temperature to stop SA')
    parser.add_argument('--schedule', choices=['exponential', 'linear'], default='exponential',
                        help='Cooling schedule for SA')
    # Parametry dla GA
    parser.add_argument('--pop-size', type=int, default=100,
                        help='Population size for GA')
    parser.add_argument('--crossover', choices=['one_point', 'uniform'], default='one_point',
                        help='Crossover type for GA')
    parser.add_argument('--mutation', choices=['flip', 'swap'], default='flip',
                        help='Mutation type for GA')
    return parser.parse_args()


def main():
    args = parse_args()

    # Ustaw ziarno RNG
    if args.seed is not None:
        random.seed(args.seed)

    # Wczytaj problem
    problem = SubsetSum.from_file(args.input)
    if args.target is not None:
        problem.target = args.target

    # Dispatcher algorytmu
    start_time = time.time()
    # Każdy algorytm zwraca teraz (best_sol, best_obj) lub (best_sol, best_obj, history)
    result = None
    if args.algorithm == 'full':
        best_sol, best_obj = full_search(problem, time_limit=args.time_limit)
        history = [(time.time() - start_time, best_obj)]
    elif args.algorithm == 'hill':
        neigh = flip_neighbor if args.neighborhood == 'flip' else all_neighbors
        best_sol, best_obj, history = hill_climb(
            problem,
            neighborhood=neigh,
            time_limit=args.time_limit,
            random_choice=args.random_choice
        )
    elif args.algorithm == 'tabu':
        neigh = all_neighbors if args.neighborhood == 'all' else flip_neighbor
        best_sol, best_obj, history = tabu_search(
            problem,
            neighborhood=neigh,
            tabu_size=args.tabu_size,
            time_limit=args.time_limit
        )
    elif args.algorithm == 'sa':
        best_sol, best_obj, history = simulated_annealing(
            problem,
            neighborhood=flip_neighbor,
            schedule=args.schedule,
            initial_temp=args.initial_temp,
            alpha=args.alpha,
            min_temp=args.min_temp,
            time_limit=args.time_limit
        )
    elif args.algorithm == 'ga':
        best_sol, best_obj, history = genetic_algorithm(
            problem,
            pop_size=args.pop_size,
            crossover=args.crossover,
            mutation=args.mutation,
            time_limit=args.time_limit
        )
    else:
        print(f"Unknown algorithm: {args.algorithm}")
        sys.exit(1)

    elapsed = time.time() - start_time

    # Wyświetlenie wyników końcowych
    total = sum(val for val, bit in zip(problem.values, best_sol) if bit)
    print('Best solution:', best_sol)
    print('Sum:', total)
    print('|Sum - Target|:', best_obj)
    print(f'Elapsed time: {elapsed:.2f}s')

    # Zapisywanie historii do CSV
    logs_dir = Path('experiments') / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    instance_name = Path(args.input).stem
    log_file = logs_dir / f"{instance_name}_{args.algorithm}.csv"
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'best_obj'])
        for t, obj in history:
            writer.writerow([f"{t:.4f}", obj])
    print(f"History saved to {log_file}")


if __name__ == '__main__':
    main()