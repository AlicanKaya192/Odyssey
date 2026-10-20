def workers_needed(rate, service_ms, target):
    workers = 1
    while rate * service_ms / 1000 / workers > target:
        workers += 1
    return workers


print(workers_needed(50, 10, 0.7))
print(workers_needed(120, 10, 0.7))
print(workers_needed(300, 45, 0.7))
