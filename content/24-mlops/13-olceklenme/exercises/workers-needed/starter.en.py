def workers_needed(rate, service_ms, target):
    # Add workers until the utilization drops below the target.
    pass


print(workers_needed(50, 10, 0.7))
print(workers_needed(120, 10, 0.7))
print(workers_needed(300, 45, 0.7))
