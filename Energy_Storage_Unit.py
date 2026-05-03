class Energy_Storage_Unit:
    """
    Simulates the battery/supercapacitor behavior.
    Enforces capacity limits and the safety threshold Emin.
    """
    def __init__(self, capacity, e_min, initial_energy=None):
        self.capacity = capacity  # Maximum capacity (C)
        self.e_min = e_min        # Minimum energy threshold (Emin)
        
        # Initial energy is typically full capacity unless specified
        if initial_energy is None:
            self.current_energy = capacity
        else:
            self.current_energy = initial_energy

    def update(self, harvested_amount, consumed_amount):
        """
        Updates the battery level for a single time step.
        """
        # 1. Add harvested energy and cap at maximum capacity C
        self.current_energy = min(self.capacity, self.current_energy + harvested_amount)
        
        # 2. Subtract energy consumed by the CPU
        self.current_energy -= consumed_amount
        
        # 3. Check for battery depletion (system failure)
        # In a real simulation, if current_energy < e_min, the run is marked 
        # as a failure for the DSR calculation.
        return self.current_energy

    def is_depleted(self):
        """
        Checks if the energy has dropped below the safety threshold.
        """
        return self.current_energy < self.e_min