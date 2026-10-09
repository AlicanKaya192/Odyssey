from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base, height):
        self.base, self.height = base, height

    def area(self):
        return self.base * self.height / 2


def total_area(specs):
    kinds = {"rect": Rectangle, "tri": Triangle}
    shapes = [kinds[kind](a, b) for kind, a, b in specs]
    return sum(s.area() for s in shapes)

print(total_area([["rect", 3, 4], ["tri", 6, 2]]))
