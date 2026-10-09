def knapsack(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]
            if weight <= w and best[i - 1][w - weight] + value > best[i][w]:
                best[i][w] = best[i - 1][w - weight] + value
    return best[n][capacity]


print(knapsack([[60, 10], [100, 20], [120, 30]], 50))
print(knapsack([[10, 5], [40, 4], [30, 6], [50, 3]], 10))
big = [[(i * 37) % 97 + 1, (i * 53) % 61 + 1] for i in range(100)]
print(knapsack(big, 2000))
