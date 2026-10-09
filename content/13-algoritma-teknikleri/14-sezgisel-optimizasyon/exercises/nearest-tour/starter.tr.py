import math


def nearest_tour(pts, start):
    tour = [start]
    left = set(range(len(pts))) - {start}
    # left bitene kadar en yakini ekle.
    return tour

pts = [(0, 0), (5, 0), (1, 1), (6, 1), (2, 0)]
print(nearest_tour(pts, 0))
print(nearest_tour(pts, 3))
