import random

def uunifast_discard(n, u_total):
    """Standard UUnifast algorithm for task utilization distribution"""
    utilizations = []
    sum_u = u_total
    for i in range(1, n):
        next_u = sum_u * (random.random() ** (1.0 / (n - i)))
        utilizations.append(sum_u - next_u)
        sum_u = next_u
    utilizations.append(sum_u)
    return utilizations

# Example usage for a task set of 5 tasks with 0.6 total utilization
print(f"Generated Task Set Utilizations: {uunifast_discard(5, 0.6)}")