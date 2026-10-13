def threshold_report(inside, outside, loss):
    threshold = sorted(inside)[int(loss * len(inside))]
    kept = sum(s >= threshold for s in inside) / len(inside)
    rejected = sum(s < threshold for s in outside) / len(outside)
    return [threshold, round(kept, 3), round(rejected, 3)]

inside = [0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.2]
outside = [0.1, 0.25, 0.32, 0.5, 0.05]
print(threshold_report(inside, outside, 0.1))
print(threshold_report(inside, outside, 0.3))
