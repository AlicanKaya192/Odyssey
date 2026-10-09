def fractional_knapsack(items, capacity):
    total = 0
    for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if capacity <= 0:
            break
        take = min(weight, capacity)
        total += value * take / weight
        capacity -= take
    return round(total, 2)


print(fractional_knapsack([[60, 10], [100, 20], [120, 30]], 50))
print(fractional_knapsack([[10, 4], [7, 3]], 5))
