class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def count_unique(pairs):
    points = set()
    for x, y in pairs:
        points.add(Point(x, y))
    return len(points)


print(count_unique([[1, 2], [3, 4], [1, 2], [1, 2]]))
print(count_unique([]))
print(Point(5, 6) == Point(5, 6))
