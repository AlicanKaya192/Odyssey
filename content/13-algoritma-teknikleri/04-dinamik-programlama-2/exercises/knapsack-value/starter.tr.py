def knapsack(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    # Her esya, her kapasite: al ya da alma.
    return best[n][capacity]


print(knapsack([[60, 10], [100, 20], [120, 30]], 50))
print(knapsack([[10, 5], [40, 4], [30, 6], [50, 3]], 10))
big = [[(i * 37) % 97 + 1, (i * 53) % 61 + 1] for i in range(100)]
print(knapsack(big, 2000))
