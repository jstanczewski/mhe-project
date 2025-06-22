import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    # Ścieżka do katalogu z logami
    logs_dir = Path('experiments') / 'logs'
    if not logs_dir.exists():
        print(f"No logs directory found at {logs_dir}")
        return

    # Wczytaj wszystkie pliki CSV z logami
    log_files = sorted(logs_dir.glob('*.csv'))
    if not log_files:
        print("No log files to plot.")
        return

    # Grupowanie plików według wielkości instancji (prefix przed '_')
    instances = {}
    for file in log_files:
        stem = file.stem  # np. 'small_hill_det'
        parts = stem.split('_', 1)
        if len(parts) != 2:
            continue
        inst, alg = parts
        instances.setdefault(inst, []).append((alg, file))

    # Generowanie oddzielnego wykresu dla każdej instancji
    for inst, alg_files in instances.items():
        plt.figure(figsize=(8, 5))
        for alg, file in alg_files:
            df = pd.read_csv(file)
            plt.plot(df['time'], df['best_obj'], label=alg)

        plt.xlabel('Time (s)')
        plt.ylabel('|Sum – Target|')
        plt.title(f'Convergence Curves for {inst.capitalize()} Instance')
        plt.legend()
        plt.tight_layout()

        # Zapis wykresu do pliku
        output_file = logs_dir.parent / f'convergence_{inst}.png'
        plt.savefig(output_file)
        print(f"Saved plot for '{inst}' to {output_file}")
        plt.close()

if __name__ == '__main__':
    main()
