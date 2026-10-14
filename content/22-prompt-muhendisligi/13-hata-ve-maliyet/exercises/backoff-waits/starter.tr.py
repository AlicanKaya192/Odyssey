def backoff_waits(attempts, base, cap):
    return []


print(backoff_waits(4, 1.0, 30.0))
print(backoff_waits(7, 0.5, 8.0))
print(backoff_waits(1, 1.0, 30.0))
