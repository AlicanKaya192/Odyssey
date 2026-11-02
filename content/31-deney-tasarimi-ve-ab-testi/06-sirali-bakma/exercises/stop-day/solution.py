def stop_day(p_values, threshold):
    for i, p in enumerate(p_values):
        if p < threshold:
            return i + 1
    return 0


print(stop_day([0.3, 0.2, 0.004, 0.001], 0.0074))
print(stop_day([0.3, 0.2, 0.1], 0.0074))
