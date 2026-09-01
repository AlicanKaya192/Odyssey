import math


class Shape:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return self.name + " has area " + str(self.area())


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("circle")
        self.radius = radius

    def area(self):
        return round(math.pi * self.radius * self.radius, 2)


print(Rectangle(3, 4).describe())
print(Circle(2).describe())
