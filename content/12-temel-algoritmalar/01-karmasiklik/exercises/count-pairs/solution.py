def count_pairs(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count


for n in [10, 100, 1000]:
    print(n, count_pairs(n), n * (n - 1) // 2)
