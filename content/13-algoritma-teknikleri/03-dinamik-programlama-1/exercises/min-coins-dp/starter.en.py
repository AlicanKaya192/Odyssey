def min_coins(amount, coins):
    best = [0] + [float("inf")] * amount
    # Try every coin for every amount.
    return -1


print(min_coins(6, [1, 3, 4]))
print(min_coins(11, [2, 5]))
print(min_coins(3, [2]))
print(min_coins(9999, [1, 7, 23, 97, 211]))
