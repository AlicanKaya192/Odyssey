def best_items(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    # 1. Fill the table.  2. Walk backwards from the end.
    chosen = []
    return sorted(chosen)


print(best_items([[60, 10], [100, 20], [120, 30]], 50))
print(best_items([[10, 5], [40, 4], [30, 6], [50, 3]], 10))
