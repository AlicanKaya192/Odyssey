import math


def clusters(points, k):
    n = len(points)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    pairs = sorted((math.dist(points[i], points[j]), i, j)
                   for i in range(n) for j in range(i + 1, n))
    for d, i, j in pairs:
        if groups <= k:
            break
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            groups -= 1
    result = {}
    for i in range(n):
        result.setdefault(find(i), []).append(i)
    return sorted(result.values())

points = [(0, 0), (1, 0), (0, 1), (6, 6), (7, 6),
          (12, 0), (13, 1), (6, 7)]
for group in clusters(points, 3):
    print(group)
print(clusters(points, 1))
