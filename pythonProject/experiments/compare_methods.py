import subprocess
import csv
import time
from pathlib import Path

# Konfiguracja instancji
TEST_INSTANCES = [
    # ('huge', 'data/huge.txt'),
    ('large', 'data/large.txt'),
    ('medium', 'data/medium.txt'),
    # ('small', 'data/small.txt'),
]

# Parametry dla algorytmów
SA_EXP_PARAMS = {
    'schedule': 'exponential',
    'initial_temp': '500',
    'alpha': '0.8',
    'min_temp': '0.01'
}
SA_LIN_PARAMS = {
    'schedule': 'linear',
    'initial_temp': '100',
    'alpha': '0.1',
    'min_temp': '0.01'
}
TABU_PARAMS = {
    'tabu_size': '3'
}

# Definicja algorytmów do porównania (bez GA)
ALGORITHMS = [
    ('full', ['--algorithm', 'full']),
    # ('hill_det', ['--algorithm', 'hill', '--neighborhood', 'all']),
    # ('hill_rand', ['--algorithm', 'hill', '--neighborhood', 'all', '--random-choice']),
    # ('tabu',     ['--algorithm', 'tabu', '--neighborhood', 'all', '--tabu-size', TABU_PARAMS['tabu_size']]),
    # ('sa_exp',   ['--algorithm', 'sa',
    #               '--schedule', SA_EXP_PARAMS['schedule'],
    #               '--initial-temp', SA_EXP_PARAMS['initial_temp'],
    #               '--alpha', SA_EXP_PARAMS['alpha'],
    #               '--min-temp', SA_EXP_PARAMS['min_temp']]),
    # ('sa_lin',   ['--algorithm', 'sa',
    #               '--schedule', SA_LIN_PARAMS['schedule'],
    #               '--initial-temp', SA_LIN_PARAMS['initial_temp'],
    #               '--alpha', SA_LIN_PARAMS['alpha'],
    #               '--min-temp', SA_LIN_PARAMS['min_temp']]),
]

CLI_SCRIPT = ['python', '-m', 'solver.cli']
OUTPUT_CSV = Path(__file__).parent.parent / 'results.csv'
LOGS_DIR = Path(__file__).parent.parent / 'experiments' / 'logs'


def main():
    # Upewnij się, że katalog na logi istnieje
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['instance', 'algorithm', 'seed', 'time_limit', 'sum_diff', 'elapsed'])

        for name, path in TEST_INSTANCES:
            for alg_name, alg_args in ALGORITHMS:
                default_args = ['--input', path, '--seed', '1', '--time-limit', '60']
                # Dodajemy flagę label, by CLI zapisalo log pod odpowiednią nazwą
                label_arg = ['--label', alg_name]
                cmd = CLI_SCRIPT + label_arg + alg_args + default_args
                print(f"Running: {cmd}")
                start_time = time.time()
                result = subprocess.run(cmd, capture_output=True, text=True)
                elapsed = time.time() - start_time

                if result.returncode != 0:
                    print(f"Error running {alg_name} on {name}: {result.stderr}")
                    continue

                # Parsowanie wyniku |Sum - Target|
                sum_diff = None
                for line in result.stdout.strip().splitlines():
                    if line.startswith('|Sum'):
                        parts = line.split(':')
                        if len(parts) == 2:
                            sum_diff = parts[1].strip()

                # Zapis do głównego CSV
                writer.writerow([name, alg_name, 1, 2, sum_diff, f"{elapsed:.2f}"])

    print(f"Results saved to {OUTPUT_CSV}")


if __name__ == '__main__':
    main()
