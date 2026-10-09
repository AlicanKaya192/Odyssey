import math


def closest(points):
    n = len(points)
    if n <= 3:
        return min((math.dist(p, q) for i, p in enumerate(points)
                    for q in points[i + 1:]), default=math.inf)
    mid = n // 2
    mid_x = points[mid][0]
    d = min(closest(points[:mid]), closest(points[mid:]))
    strip = sorted((p for p in points if abs(p[0] - mid_x) < d), key=lambda p: p[1])
    for i, p in enumerate(strip):
        for q in strip[i + 1:]:
            if q[1] - p[1] >= d:
                break
            d = min(d, math.dist(p, q))
    return d


def closest_distance(points):
    return round(closest(sorted(tuple(p) for p in points)), 6)


print(closest_distance([[0, 0], [5, 5], [1, 1], [9, 0], [5, 6]]))
pts = [[(i * 7919) % 10007, (i * 104729) % 10009] for i in range(30_000)]
print(closest_distance(pts))
