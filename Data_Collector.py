import numpy as np
import pandas as pd
from scipy import stats

class Data_Collector:
    """
    Handles data aggregation, statistical calculation (95% CI),
    and determination of Cmin for the Feasibility Surface.
    """
    def __init__(self):
        self.raw_data = []

    def collect_run_results(self, rho, capacity, dsr_list):
        """
        Processes a batch of 1,000 runs for a specific configuration.
        """
        dsr_array = np.array(dsr_list)
        mean_dsr = np.mean(dsr_array)
        
        # Calculate 95% Confidence Interval
        # Formula: CI = mean +/- (t_critical * (std / sqrt(n)))
        n = len(dsr_array)
        std_err = stats.sem(dsr_array) # Standard error of the mean
        confidence = 0.95
        h = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
        
        result = {
            'rho': rho,
            'capacity': capacity,
            'mean_dsr': mean_dsr,
            'ci_lower': mean_dsr - h,
            'ci_upper': mean_dsr + h,
            'is_feasible': 1 if mean_dsr >= 1.0 else 0
        }
        self.raw_data.append(result)
        return result

    def get_c_min(self, df):
        """
        Identifies the minimum capacity C where DSR reaches 1.0 
        for each replenishment ratio rho.
        """
        c_min_results = []
        for rho in df['rho'].unique():
            subset = df[df['rho'] == rho]
            # Find capacities where mean_dsr is 1.0
            feasible_configs = subset[subset['mean_dsr'] >= 1.0]
            
            if not feasible_configs.empty:
                c_min = feasible_configs['capacity'].min()
                c_min_results.append({'rho': rho, 'Cmin': c_min})
            else:
                # If no configuration reached DSR 1.0 in the tested range
                c_min_results.append({'rho': rho, 'Cmin': None})
                
        return pd.DataFrame(c_min_results)

    def save_to_csv(self, filename="processed_results.csv"):
        """
        Saves the aggregated statistical results to a CSV file.
        """
        df = pd.DataFrame(self.raw_data)
        df.to_csv(filename, index=False)
        
        # Also save a summary of Cmin for the Feasibility Surface plot
        cmin_df = self.get_c_min(df)
        cmin_df.to_csv("cmin_results.csv", index=False)
        print(f"Data saved to {filename} and cmin_results.csv")