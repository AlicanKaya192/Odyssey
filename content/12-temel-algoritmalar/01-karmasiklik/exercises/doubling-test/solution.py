def count_triples(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                count += 1
    return count


previous = None
for n in [10, 20, 40, 80]:
    current = count_triples(n)
    if previous is None:
        print(n, current)
    else:
        print(n, current, round(current / previous, 2))
    previous = current
