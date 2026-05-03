import numpy as np
import pandas as pd
from PAH_Supervisor import PAH_Supervisor
from RM_Scheduler import RM_Scheduler
from Energy_Storage_Unit import Energy_Storage_Unit
from Energy_Harvester_Model import Energy_Harvester
# Assuming these exist based on your previous descriptions
from Task_Generator import generate_uunifast_tasks
from Job_Set_Builder import build_job_set

def run_simulation(rho, capacity, e_min, task_set, duration):
    """
    Executes a single simulation run for a specific task set.
    """
    # Initialize components
    harvester = Energy_Harvester(rho)
    storage = Energy_Storage_Unit(capacity, e_min)
    supervisor = PAH_Supervisor(rho, capacity, e_min)
    scheduler = RM_Scheduler(supervisor)
    
    # Generate job instances from the periodic tasks
    job_set = build_job_set(task_set, duration)
    
    success_count = 0
    total_jobs = len(job_set)
    
    for t in range(duration):
        # 1. Scheduler picks a job (checked against Supervisor)
        current_job, status = scheduler.schedule(t, job_set, storage.current_energy)
        
        # 2. Determine energy consumption (Pc = 1 if job runs, 0 otherwise)
        consumed = 1 if status == "EXECUTING" else 0
        harvested = harvester.get_harvested_energy(1)
        
        # 3. Update job progress if executing
        if status == "EXECUTING":
            scheduler.execute_job(current_job)
            
        # 4. Update battery state
        storage.update(harvested, consumed)
        
        # 5. Check for failure (energy depletion)
        if storage.is_depleted():
            return 0.0  # DSR is 0 if battery dies
            
    # Calculate Deadline Success Ratio (DSR)
    # A job is successful if its c_rem == 0 by its deadline
    successful_jobs = sum(1 for j in job_set if j.c_rem <= 0)
    return successful_jobs / total_jobs

def main():
    # Experimental Setup from the paper
    RHO_VALUES = [1.0, 1.2, 1.4]
    CAPACITIES = np.linspace(100, 2000, 20)  # Range of battery sizes
    NUM_RUNS = 1000
    UTILIZATION = 0.6
    E_MIN = 0
    T_SIM = 10000  # Simulation horizon
    
    results = []

    print(f"Starting experiments for U={UTILIZATION}...")
    
    for rho in RHO_VALUES:
        for C in CAPACITIES:
            dsr_list = []
            for run in range(NUM_RUNS):
                # Generate a new synthetic task set for each run
                tasks = generate_uunifast_tasks(n=5, u_total=UTILIZATION)
                
                # Run the simulation
                dsr = run_simulation(rho, C, E_MIN, tasks, T_SIM)
                dsr_list.append(dsr)
            
            # Aggregate data
            avg_dsr = np.mean(dsr_list)
            results.append({
                'rho': rho,
                'capacity': C,
                'avg_dsr': avg_dsr
            })
            print(f"Completed: rho={rho}, C={C:.0f} -> Avg DSR: {avg_dsr:.4f}")

    # Save results for Plot_Results.py
    df = pd.DataFrame(results)
    df.to_csv("experiment_results.csv", index=False)
    print("Results saved to experiment_results.csv")

if __name__ == "__main__":
    main()