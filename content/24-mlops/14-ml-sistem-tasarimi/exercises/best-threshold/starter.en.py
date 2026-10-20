def best_threshold(probs, labels, candidates, saved, cost):
    # Profit for every threshold; keep the largest.
    pass


probs = [0.9, 0.6, 0.4, 0.35, 0.2, 0.1]
labels = [1, 0, 1, 1, 0, 0]
print(best_threshold(probs, labels, [0.3, 0.5, 0.7], 18, 5))
print(best_threshold(probs, labels, [0.3, 0.5, 0.7], 4, 5))
