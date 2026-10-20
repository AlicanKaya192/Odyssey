def profit(probs, labels, threshold, saved, cost):
    offers, total = 0, 0
    for p, y in zip(probs, labels):
        if p >= threshold:
            offers += 1
            total += saved * y - cost
    return [offers, total]


probs = [0.9, 0.6, 0.4, 0.2, 0.1]
labels = [1, 0, 1, 0, 0]
print(profit(probs, labels, 0.5, 18, 5))
print(profit(probs, labels, 0.3, 18, 5))
print(profit(probs, labels, 0.95, 18, 5))
