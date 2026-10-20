def needs_retrain(live, base, drift, max_drop, max_drift):
    return live < base - max_drop or drift > max_drift


print(needs_retrain(0.813, 0.813, 0.07, 0.05, 0.25))
print(needs_retrain(0.778, 0.813, 0.578, 0.05, 0.25))
print(needs_retrain(0.691, 0.782, 0.2, 0.05, 0.25))
