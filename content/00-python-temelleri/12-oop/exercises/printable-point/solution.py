import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance(self):
        return round(math.sqrt(self.x * self.x + self.y * self.y), 2)


spot = Point(3, 4)

print(spot)
print(spot.distance())
