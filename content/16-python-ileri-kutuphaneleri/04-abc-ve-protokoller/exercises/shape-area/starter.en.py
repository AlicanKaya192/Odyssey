from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


# Rectangle and Triangle


def total_area(specs):
    return 0

print(total_area([["rect", 3, 4], ["tri", 6, 2]]))
