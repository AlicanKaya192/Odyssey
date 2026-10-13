def threshold_report(inside, outside, loss):
    return []

inside = [0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.2]
outside = [0.1, 0.25, 0.32, 0.5, 0.05]
print(threshold_report(inside, outside, 0.1))
print(threshold_report(inside, outside, 0.3))
