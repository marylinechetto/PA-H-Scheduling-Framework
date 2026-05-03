import numpy as np

class PAH_Supervisor:
    def __init__(self, rho, capacity, e_min):
        self.rho = rho
        self.capacity = capacity
        self.e_min = e_min
        self.p_p = rho  # Normalized harvesting rate (P_p)

    def get_slack_time(self, t, job_j, all_jobs):
        """
        Calculates ST_j(t) by replacing 'energy' with 'time'.
        Interval: [t, d_j]
        Formula: (d_j - t) - Sum(C_rem_k) for all k interfering with j.
        """
        d_j = job_j.deadline
        
        # Sum of remaining execution time for all jobs that 
        # interfere with J_j (higher priority and within the window)
        workload_demand = sum(
            k.c_rem for k in all_jobs 
            if k.priority <= job_j.priority 
            and k.arrival < d_j 
            and k.deadline <= d_j
            and k.c_rem > 0
        )
        
        # Available time in interval [t, d_j] minus the demand
        st = (d_j - t) - workload_demand
        return st

    def get_slack_energy(self, t, job_j, all_jobs, current_energy):
        """
        Calculates SE_j(t).
        Interval: [t, d_j]
        Formula: (E_initial + E_harvested) - Sum(E_rem_k) for all k interfering with j.
        """
        d_j = job_j.deadline
        
        # Sum of remaining energy for all jobs that 
        # interfere with J_j (higher priority and within the window)
        energy_demand = sum(
            k.e_rem for k in all_jobs 
            if k.priority <= job_j.priority 
            with k.arrival < d_j 
            and k.deadline <= d_j
            and k.e_rem > 0
        )
        
        # Initial energy + energy harvested in [t, d_j], capped by capacity C
        e_harvested = (d_j - t) * self.p_p
        se = min(current_energy + e_harvested, self.capacity) - energy_demand
        return se

    def get_preemption_slack_energy(self, t, job_i, all_jobs, current_energy):
        """
        Equation 5: PSE_i(t) = min(SE_k(t)) 
        For all future higher-priority jobs k that arrive before d_i.
        """
        preemptors = [
            k for k in all_jobs 
            if k.priority < job_i.priority 
            and t < k.arrival < job_i.deadline
        ]
        
        if not preemptors:
            return float('inf')

        # Compute SE for every potential preempting job
        return min(self.get_slack_energy(t, k, all_jobs, current_energy) for k in preemptors)[cite: 1]

    def can_execute(self, t, job_i, all_jobs, current_energy):
        """
        Meta-scheduling rule for RM-H.
        """
        st = self.get_slack_time(t, job_i, all_jobs)
        se = self.get_slack_energy(t, job_i, all_jobs, current_energy)
        pse = self.get_preemption_slack_energy(t, job_i, all_jobs, current_energy)

        # A job J_i can only run if its own time/energy is safe AND 
        # it doesn't jeopardize future higher-priority jobs (PSE).
        if st >= 0 and se >= self.e_min and pse >= self.e_min:
            return True
        return False