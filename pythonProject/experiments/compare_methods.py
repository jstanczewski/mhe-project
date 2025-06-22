import subprocess
import csv
import time
from pathlib import Path

# Konfiguracja instancji i algorytmów do porównania
test_instances = [
    ('small', 'data/small.txt'),
    ('medium', 'data/medium.txt'),
    ('large', 'data/large.txt'),
    ('huge', 'data/huge.txt'),
]

# Każdy algorytm zawiera listę argumentów CLI, w tym --algorithm
algorithms = [
#    ('full', ['--algorithm', 'full']),
    ('hill_det', ['--algorithm', 'hill', '--neighborhood', 'all']),
    ('hill_rand', ['--algorithm', 'hill', '--neighborhood', 'all', '--random-choice']),
    ('tabu', ['--algorithm', 'tabu', '--neighborhood', 'all', '--tabu-size', '20']),
    ('sa_exp', ['--algorithm', 'sa', '--schedule', 'exponential', '--initial-temp', '500', '--alpha', '0.8', '--min-temp', '0.01']),
    ('sa_lin', ['--algorithm', 'sa', '--schedule', 'linear', '--initial-temp', '100', '--alpha', '0.1', '--min-temp', '0.01']),
    ('ga', ['--algorithm', 'ga', '--pop-size', '50', '--crossover', 'uniform', '--mutation', 'flip']),
]

# Ścieżka do skryptu CLI
cli_script = ['python', '-m', 'solver.cli']

# Plik wyjściowy CSV
generated_dir = Path(__file__).parent.parent
output_csv = generated_dir / 'results.csv'

with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Nagłówek
    writer.writerow(['instance', 'algorithm', 'seed', 'time_limit', 'sum_diff', 'elapsed'])

    for name, path in test_instances:
        for alg_name, alg_args in algorithms:
            # Parametry wspólne
            default_args = ['--input', path, '--seed', '1', '--time-limit', '2']
            cmd = cli_script + alg_args + default_args
            print(f"Running: {cmd}")
            start = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True)
            elapsed = time.time() - start

            if result.returncode != 0:
                print(f"Error running {alg_name} on {name}: {result.stderr}")
                continue

            # Parsowanie wyniku |Sum - Target|
            lines = result.stdout.strip().splitlines()
            sum_diff = None
            for line in lines:
                if line.startswith('|Sum'):
                    parts = line.split(':')
                    if len(parts) == 2:
                        sum_diff = parts[1].strip()
            writer.writerow([name, alg_name, 1, 2, sum_diff, f"{elapsed:.2f}"])

print(f"Results saved to {output_csv}")
