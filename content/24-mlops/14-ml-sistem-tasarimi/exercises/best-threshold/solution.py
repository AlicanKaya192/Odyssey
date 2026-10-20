def best_threshold(probs, labels, candidates, saved, cost):
    best, best_total = None, None
    for threshold in candidates:
        total = 0
        for p, y in zip(probs, labels):
            if p >= threshold:
                total += saved * y - cost
        if best_total is None or total > best_total:
            best, best_total = threshold, total
    return [best, best_total]


probs = [0.9, 0.6, 0.4, 0.35, 0.2, 0.1]
labels = [1, 0, 1, 1, 0, 0]
print(best_threshold(probs, labels, [0.3, 0.5, 0.7], 18, 5))
print(best_threshold(probs, labels, [0.3, 0.5, 0.7], 4, 5))
