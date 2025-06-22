import subprocess
import csv
import time
from pathlib import Path

# Configuration of test instances: (label, file path)
TEST_INSTANCES = [
    ('huge', 'data/huge.txt'),
    ('large', 'data/large.txt'),
    # ('medium', 'data/medium.txt'),  # optional smaller tests
    # ('small', 'data/small.txt'),
]

# Parameters for algorithms
SA_EXP_PARAMS = {
    'schedule': 'exponential',      # exponential cooling schedule
    'initial_temp': '500',          # starting temperature
    'alpha': '0.95',                # cooling rate
    'min_temp': '0.0001'            # minimum temperature
}
SA_LIN_PARAMS = {
    'schedule': 'linear',           # linear cooling schedule
    'initial_temp': '500',
    'alpha': '1',                   # linear decrement per step
    'min_temp': '0.001'
}
TABU_PARAMS = {
    'tabu_size': '3'                # size of the tabu list
}

# Algorithms to compare
# Each tuple: (label, CLI argument list)
ALGORITHMS = [
    # ('full',     ['--algorithm', 'full']),
    # ('hill_det', ['--algorithm', 'hill', '--neighborhood', 'all']),
    # ('hill_rand',['--algorithm', 'hill', '--neighborhood', 'all', '--random-choice']),
    # ('tabu',     ['--algorithm', 'tabu', '--neighborhood', 'all', '--tabu-size', TABU_PARAMS['tabu_size']]),
    ('sa_exp',   [
        '--algorithm', 'sa',
        '--schedule', SA_EXP_PARAMS['schedule'],
        '--initial-temp', SA_EXP_PARAMS['initial_temp'],
        '--alpha', SA_EXP_PARAMS['alpha'],
        '--min-temp', SA_EXP_PARAMS['min_temp'],
    ]),
    ('sa_lin',   [
        '--algorithm', 'sa',
        '--schedule', SA_LIN_PARAMS['schedule'],
        '--initial-temp', SA_LIN_PARAMS['initial_temp'],
        '--alpha', SA_LIN_PARAMS['alpha'],
        '--min-temp', SA_LIN_PARAMS['min_temp'],
    ]),
]

CLI_SCRIPT = ['python', '-m', 'solver.cli']
OUTPUT_CSV = Path(__file__).parent.parent / 'results.csv'
LOGS_DIR = Path(__file__).parent.parent / 'experiments' / 'logs'


def main():
    # Ensure the logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Open summary CSV for writing overall results
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write CSV header
        writer.writerow(['instance', 'algorithm', 'seed', 'time_limit', 'sum_diff', 'elapsed'])

        # Loop over each test instance
        for name, path in TEST_INSTANCES:
            # Loop over each algorithm variant
            for alg_name, alg_args in ALGORITHMS:
                # Common CLI arguments for all runs
                default_args = ['--input', path, '--seed', '1', '--time-limit', '60']
                # Include custom label so logs are named accordingly
                label_arg = ['--label', alg_name]
                # Construct full command
                cmd = CLI_SCRIPT + label_arg + alg_args + default_args
                print(f"Running: {cmd}")

                start_time = time.time()
                result = subprocess.run(cmd, capture_output=True, text=True)
                elapsed = time.time() - start_time

                # Handle CLI errors gracefully
                if result.returncode != 0:
                    print(f"Error running {alg_name} on {name}: {result.stderr}")
                    continue

                # Parse the final |Sum - Target| from CLI output
                sum_diff = None
                for line in result.stdout.strip().splitlines():
                    if line.startswith('|Sum'):
                        parts = line.split(':')
                        if len(parts) == 2:
                            sum_diff = parts[1].strip()

                # Append a row to the summary CSV
                writer.writerow([name, alg_name, 1, 60, sum_diff, f"{elapsed:.2f}"])

    print(f"Results saved to {OUTPUT_CSV}")


if __name__ == '__main__':
    main()
