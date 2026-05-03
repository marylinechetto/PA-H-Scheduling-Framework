import numpy as np
import random

def generate_uunifast_tasks(n, u_total):
    """
    UUnifast algorithm: Generates n utilizations summing to u_total.
    """
    utilizations = []
    sum_u = u_total
    for i in range(1, n):
        # The core UUnifast formula
        next_sum_u = sum_u * (random.random() ** (1.0 / (n - i)))
        utilizations.append(sum_u - next_sum_u)
        sum_u = next_sum_u
    utilizations.append(sum_u)
    
    # Assign periods and compute execution times (C_i = U_i * T_i)
    tasks = []
    for i, u_i in enumerate(utilizations):
        # Periods are typically chosen from a range, e.g., 100 to 1000
        period = random.randint(100, 1000)
        tasks.append({
            'id': i,
            'period': period,
            'deadline': period,
            'wcet': max(1, round(u_i * period)), # C_i
            'energy': max(1, round(u_i * period)), # E_i (assuming Pc = 1)
            'priority': i # Static RM priority (set later by period)
        })
    
    # Sort by period to assign RM priorities (shortest period = priority 0)
    tasks.sort(key=lambda x: x['period'])
    for idx, task in enumerate(tasks):
        task['priority'] = idx
        
    return tasks