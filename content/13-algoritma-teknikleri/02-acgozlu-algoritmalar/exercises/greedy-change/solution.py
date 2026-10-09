def greedy_change(amount, coins):
    used = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            used.append(coin)
    return used


print(greedy_change(87, [1, 5, 10, 25, 50]))
print(greedy_change(6, [4, 1, 3]))
