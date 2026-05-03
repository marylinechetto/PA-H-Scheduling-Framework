class Energy_Harvester:
    """
    Simulates the energy harvesting source.
    Based on the Replenishment Ratio (rho), it provides a constant power flow.
    """
    def __init__(self, rho):
        # rho = Pp / Pc. 
        # Since we normalize consumption power (Pc) to 1, Pp equals rho.
        self.p_p = rho 

    def get_harvested_energy(self, duration):
        """
        Returns the amount of energy produced over a given time duration.
        """
        return self.p_p * duration