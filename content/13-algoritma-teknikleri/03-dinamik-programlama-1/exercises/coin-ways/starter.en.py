def count_ways(amount, coins):
    ways = [1] + [0] * amount
    # The outer loop is the coins, the inner loop the amounts.
    return ways[amount]


print(count_ways(10, [1, 2, 5]))
print(count_ways(100, [1, 5, 10, 25, 50]))
print(count_ways(1000, [1, 2, 5, 10, 20, 50, 100, 200]))
