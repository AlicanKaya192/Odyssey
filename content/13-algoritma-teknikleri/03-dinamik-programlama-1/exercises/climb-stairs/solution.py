def ways_to_climb(n):
    ways = [1] * (n + 1)
    for i in range(2, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    return ways[n]


for n in [1, 2, 3, 4, 5]:
    print(n, ways_to_climb(n))
print(90, ways_to_climb(90))
