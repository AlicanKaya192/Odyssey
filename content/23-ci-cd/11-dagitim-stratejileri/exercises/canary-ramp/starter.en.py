def ramp(old, stages, max_increase=0.01, min_requests=500):
    # Compute the old rate once, then go through the steps in order.
    pass


old = [40, 10000]
print(ramp(old, [[5, 2, 600], [25, 10, 2500], [50, 30, 5000], [100, 50, 10000]]))
print(ramp(old, [[5, 1, 600], [25, 60, 2500], [50, 0, 5000]]))
print(ramp(old, [[5, 0, 120], [25, 0, 2500]]))
