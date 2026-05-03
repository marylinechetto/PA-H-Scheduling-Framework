class Job:
    def __init__(self, task_id, arrival, deadline, execution_time, energy, priority):
        self.task_id = task_id
        self.arrival = arrival
        self.deadline = deadline
        self.c_rem = execution_time  # Remaining Execution Time
        self.e_rem = energy          # Remaining Energy Consumption
        self.priority = priority

def build_job_set(tasks, duration):
    """
    Creates a list of all jobs released within the simulation duration.
    """
    job_set = []
    for task in tasks:
        arrival = 0
        while arrival < duration:
            job_set.append(Job(
                task_id=task['id'],
                arrival=arrival,
                deadline=arrival + task['deadline'],
                execution_time=task['wcet'],
                energy=task['energy'],
                priority=task['priority']
            ))
            arrival += task['period']
            
    # Sort all jobs by arrival time for the simulator
    job_set.sort(key=lambda x: x.arrival)
    return job_set