import math


def tour_length(tour, pts):
    total = 0
    for i in range(len(tour)):
        total += math.dist(pts[tour[i - 1]], pts[tour[i]])
    return round(total, 2)

square = [(0, 0), (0, 3), (4, 3), (4, 0)]
print(tour_length([0, 1, 2, 3], square))
print(tour_length([0, 2, 1, 3], square))
