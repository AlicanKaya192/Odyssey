import math


def closest(points):
    n = len(points)
    if n <= 3:
        return min((math.dist(p, q) for i, p in enumerate(points)
                    for q in points[i + 1:]), default=math.inf)
    # Bol, iki yariyi coz, seridi denetle.
    pass


def closest_distance(points):
    return round(closest(sorted(tuple(p) for p in points)), 6)


print(closest_distance([[0, 0], [5, 5], [1, 1], [9, 0], [5, 6]]))
pts = [[(i * 7919) % 10007, (i * 104729) % 10009] for i in range(30_000)]
print(closest_distance(pts))
