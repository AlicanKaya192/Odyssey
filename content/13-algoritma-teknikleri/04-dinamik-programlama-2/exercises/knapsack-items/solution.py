def best_items(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]
            if weight <= w and best[i - 1][w - weight] + value > best[i][w]:
                best[i][w] = best[i - 1][w - weight] + value
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if best[i][w] != best[i - 1][w]:
            chosen.append(i - 1)
            w -= items[i - 1][1]
    return sorted(chosen)


print(best_items([[60, 10], [100, 20], [120, 30]], 50))
print(best_items([[10, 5], [40, 4], [30, 6], [50, 3]], 10))
