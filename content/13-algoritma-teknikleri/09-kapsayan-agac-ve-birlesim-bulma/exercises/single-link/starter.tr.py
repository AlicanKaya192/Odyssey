import math


def clusters(points, k):
    n = len(points)
    parent = list(range(n))

    def find(x):
        # Koke kadar cik (yolu kisaltarak).
        return x

    groups = n
    # Ciftleri uzakliga gore sirala ve birlestir.
    return []

points = [(0, 0), (1, 0), (0, 1), (6, 6), (7, 6),
          (12, 0), (13, 1), (6, 7)]
for group in clusters(points, 3):
    print(group)
print(clusters(points, 1))
