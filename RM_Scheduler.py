import numpy as np

class RM_Scheduler:
    """
    Dispatcher using Rate Monotonic (RM) priority assignment.
    Interacts with the PAH_Supervisor to determine if execution is safe.
    """
    def __init__(self, supervisor):
        self.supervisor = supervisor
        self.ready_queue = []

    def update_ready_queue(self, t, all_jobs):
        """
        Filters all_jobs to find those that have arrived but haven't finished.
        Sorted by RM priority (lower period/id = higher priority).
        """
        self.ready_queue = [
            j for j in all_jobs 
            if j.arrival <= t and j.c_rem > 0
        ]
        # Sort by priority: RM uses static priority based on task index/period
        self.ready_queue.sort(key=lambda x: x.priority)

    def schedule(self, t, all_jobs, current_energy):
        """
        Main scheduling logic called at each time step t.
        """
        self.update_ready_queue(t, all_jobs)

        if not self.ready_queue:
            return None, "IDLE (No Jobs)"

        # Get the highest priority job (top of the sorted queue)
        top_job = self.ready_queue[0]

        # The core of RM-H: Ask the supervisor if it's safe to run top_job
        if self.supervisor.can_execute(t, top_job, all_jobs, current_energy):
            return top_job, "EXECUTING"
        else:
            # If supervisor returns False, the processor MUST harvest energy
            return None, "IDLE (Harvesting)"

    def execute_job(self, job, time_step=1):
        """
        Simulates the execution of the job for one time unit.
        Decrements remaining time (c_rem) and remaining energy (e_rem).
        """
        if job is not None:
            # P_c is assumed to be 1 in our normalized model
            job.c_rem -= time_step
            job.e_rem -= time_step 
            return True
        return False
