def profit(probs, labels, threshold, saved, cost):
    # Olasilik ve etiketi birlikte gez.
    pass


probs = [0.9, 0.6, 0.4, 0.2, 0.1]
labels = [1, 0, 1, 0, 0]
print(profit(probs, labels, 0.5, 18, 5))
print(profit(probs, labels, 0.3, 18, 5))
print(profit(probs, labels, 0.95, 18, 5))
