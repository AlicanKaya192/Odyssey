def min_coins(amount, coins):
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == float("inf") else best[amount]


print(min_coins(6, [1, 3, 4]))
print(min_coins(11, [2, 5]))
print(min_coins(3, [2]))
print(min_coins(9999, [1, 7, 23, 97, 211]))
