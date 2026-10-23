COOKIE = "🍪"


class Jar:
    def __init__(self, capacity=12):
        # ValueError if capacity is not a non-negative int
        ...

    def __str__(self):
        # One COOKIE for each cookie in the jar
        ...

    def deposit(self, n):
        # Add n cookies; ValueError if capacity is exceeded
        ...

    def withdraw(self, n):
        # Remove n cookies; ValueError if there are not enough
        ...

    @property
    def capacity(self):
        ...

    @property
    def size(self):
        ...
