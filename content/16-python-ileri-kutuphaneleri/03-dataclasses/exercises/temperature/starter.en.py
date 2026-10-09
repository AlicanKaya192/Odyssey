from dataclasses import dataclass, field


@dataclass
class Temperature:
    celsius: float
    # fahrenheit: float = field(init=False)
    # def __post_init__(self): ...

print(Temperature(100))
try:
    Temperature(-300)
except ValueError as error:
    print("ValueError:", error)
