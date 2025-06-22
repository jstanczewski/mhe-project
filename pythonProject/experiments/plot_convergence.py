import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

LOGS_DIR = Path('experiments') / 'logs'
OUTPUT_DIR = LOGS_DIR.parent


def main():
    if not LOGS_DIR.exists():
        print(f"Logs directory not found: {LOGS_DIR}")
        return

    log_files = sorted(LOGS_DIR.glob('*.csv'))
    if not log_files:
        print(f"No log files in {LOGS_DIR}")
        return

    for log_file in log_files:
        df = pd.read_csv(log_file)
        plt.figure(figsize=(8, 5))
        plt.plot(df['time'], df['best_obj'], label=log_file.stem)
        plt.xlabel('Time (s)')
        plt.ylabel('|Sum – Target|')
        plt.title(f'Convergence: {log_file.stem}')

        # Ustawienie skali Y w zależności od instancji
        inst = log_file.stem.split('_')[0]
        max_val = df['best_obj'].max()
        plt.ylim(0, max_val * 1.1)

        plt.legend()
        plt.tight_layout()

        output_path = OUTPUT_DIR / f"{log_file.stem}.png"
        plt.savefig(output_path)
        print(f"Saved plot: {output_path}")
        plt.close()

if __name__ == '__main__':
    main()
