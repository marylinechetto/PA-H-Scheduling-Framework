import numpy as np

class PA_H_Supervisor:
    def __init__(self, capacity, p_harvest_avg):
        self.C_max = capacity
        self.p_harvest = p_harvest_avg
        
    def calculate_st(self, ready_queue, current_time):
        """Calculates Slack Time: min(d_i - t_c - remaining_C)"""
        if not ready_queue:
            return float('inf')
        slacks = [(task.deadline - current_time - task.c_rem) for task in ready_queue]
        return max(0, min(slacks))

    def calculate_pse(self, current_energy, ready_queue, look_ahead_window):
        """Calculates Preemption Slack Energy (PSE)"""
        # Energy safety margin for high priority tasks
        harvested = self.p_harvest * look_ahead_window
        consumed = sum([t.c_rem * t.p_cons for t in ready_queue])
        return current_energy + harvested - consumed

    def get_decision(self, st, pse, energy):
        """The PA-H Decision Rule"""
        if st == 0 or energy >= self.C_max:
            return "MANDATORY_BUSY"
        elif pse <= 0:
            return "MANDATORY_IDLE"
        else:
            return "ADAPTIVE" # Can be Busy or Idle based on PA rule

print("PA-H Simulation Engine Loaded.")