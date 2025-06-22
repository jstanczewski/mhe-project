import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

LOGS_DIR = Path('experiments') / 'logs'
OUTPUT_DIR = LOGS_DIR.parent


def main():
    """
    Generate convergence plots for each algorithm log in the logs directory.
    Each plot displays |Sum - Target| over elapsed time.
    """
    # Check that the logs directory exists
    if not LOGS_DIR.exists():
        print(f"Logs directory not found: {LOGS_DIR}")
        return

    # Gather all CSV log files
    log_files = sorted(LOGS_DIR.glob('*.csv'))
    if not log_files:
        print(f"No log files in {LOGS_DIR}")
        return

    # Iterate over each log file
    for log_file in log_files:
        # Read the convergence data
        df = pd.read_csv(log_file)

        # Create a new figure for this algorithm/instance
        plt.figure(figsize=(8, 5))
        # Plot best objective value vs. time
        plt.plot(df['time'], df['best_obj'], label=log_file.stem)

        # Set the axis labels and title
        plt.xlabel('Time (s)')
        plt.ylabel('|Sum – Target|')
        plt.title(f'Convergence: {log_file.stem}')

        # Determine instance type from filename prefix
        inst = log_file.stem.split('_')[0]
        max_val = df['best_obj'].max()
        upper = max_val * 1.1
        plt.ylim(0, upper)

        # Show legend and apply tight layout
        plt.legend()
        plt.tight_layout()

        # Save the plot image and close the plot
        output_path = OUTPUT_DIR / f"{log_file.stem}.png"
        plt.savefig(output_path)
        print(f"Saved plot: {output_path}")
        plt.close()


if __name__ == '__main__':
    main()
