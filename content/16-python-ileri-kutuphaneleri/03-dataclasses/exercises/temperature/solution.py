from dataclasses import dataclass, field


@dataclass
class Temperature:
    celsius: float
    fahrenheit: float = field(init=False)

    def __post_init__(self):
        if self.celsius < -273.15:
            raise ValueError("below absolute zero")
        self.fahrenheit = self.celsius * 9 / 5 + 32

print(Temperature(100))
try:
    Temperature(-300)
except ValueError as error:
    print("ValueError:", error)
