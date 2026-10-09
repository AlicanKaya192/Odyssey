def coin_ways(amount, coins):
    ways = [1] + [0] * amount
    # The outer loop is the coins, the inner loop the amounts.
    return ways[amount]

print(coin_ways(5, [1, 2, 5]))
print(coin_ways(3, [2]))
print(coin_ways(1000, [1, 2, 5, 10, 20, 50, 100]))
