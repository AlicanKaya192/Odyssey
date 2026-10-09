from abc import ABC, abstractmethod


class Formatter(ABC):
    registry: dict[str, type["Formatter"]] = {}

    def __init_subclass__(cls, name: str, **kwargs):
        super().__init_subclass__(**kwargs)
        Formatter.registry[name] = cls

    @abstractmethod
    def format(self, text: str) -> str:
        ...


# iki eklenti: class UpperFormatter(Formatter, name="upper"): ...


def apply(name, text):
    return text

print(apply("upper", "odyssey"))
print(apply("reverse", "odyssey"))
print(sorted(Formatter.registry))
