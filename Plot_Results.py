import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_paper_curves(csv_file='comparison_results.csv'):
    """
    Recreates the DSR vs. Replenishment Ratio curves.
    Expects a CSV with mean DSR and upper/lower CI bounds for each algorithm.
    """
    try:
        # Assuming the Data_Collector produces a merged file for all algorithms
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("Data file not found. Using coordinates from the LaTeX source for demonstration.")
        # Manual data entry based on your TikZ coordinates
        data = {
            'rho': [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
            'rm': [18, 42, 71, 88, 96, 98, 100],
            'rm_up': [22, 46, 75, 92, 99, 99, 100.5],
            'rm_low': [14, 38, 67, 84, 93, 97, 99.5],
            'pfp': [30, 52, 92, 100, 100, 100, 100],
            'pfp_up': [33, 55, 95, 100, 100, 100, 100],
            'pfp_low': [27, 49, 89, 100, 100, 100, 100],
            'rmh': [50, 75, 100, 100, 100, 100, 100],
            'rmh_up': [52, 77, 100, 100, 100, 100, 100],
            'rmh_low': [48, 73, 100, 100, 100, 100, 100]
        }
        df = pd.DataFrame(data)

    plt.figure(figsize=(9, 7))

    # --- 1. RM (Energy-Blind) ---
    plt.plot(df['rho'], df['rm'], color='gray', linestyle='--', marker='o', 
             label='RM', linewidth=2, markersize=6)
    plt.fill_between(df['rho'], df['rm_low'], df['rm_up'], color='gray', alpha=0.3)

    # --- 2. PFP-ASAP ---
    plt.plot(df['rho'], df['pfp'], color='red', linestyle='-', marker='^', 
             label='PFPasap', linewidth=2, markersize=6)
    plt.fill_between(df['rho'], df['pfp_low'], df['pfp_up'], color='red', alpha=0.3)

    # --- 3. RM-H (PA-H Hybrid) ---
    plt.plot(df['rho'], df['rmh'], color='blue', linestyle='-', marker='s', 
             label='RM-H', linewidth=2, markersize=6)
    plt.fill_between(df['rho'], df['rmh_low'], df['rmh_up'], color='blue', alpha=0.4)

    # --- Theoretical Limit (Sustainable Boundary) ---
    plt.plot([0.5, 1.0], [50, 100], color='black', linestyle=':', 
             linewidth=1.2, label='Theoretical Limit')

    # Figure Styling to match LaTeX PGFPlots output
    plt.xlabel('Replenishment Ratio ($\\rho$)', fontsize=12)
    plt.ylabel('DSR (%)', fontsize=12)
    plt.title('Deadline Success Ratio (DSR) under varying energy replenishment ratios', 
              fontsize=14, pad=15)
    
    plt.xlim(0.5, 2.0)
    plt.ylim(0, 110)
    plt.xticks([0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0])
    plt.yticks([0, 20, 40, 60, 80, 100])
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(loc='lower right', fontsize='medium', frameon=True)

    plt.tight_layout()
    plt.savefig('dsr_comparison_reproduced.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_paper_curves()