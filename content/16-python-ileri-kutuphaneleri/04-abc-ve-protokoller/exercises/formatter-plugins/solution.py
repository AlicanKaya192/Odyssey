from abc import ABC, abstractmethod


class Formatter(ABC):
    registry: dict[str, type["Formatter"]] = {}

    def __init_subclass__(cls, name: str, **kwargs):
        super().__init_subclass__(**kwargs)
        Formatter.registry[name] = cls

    @abstractmethod
    def format(self, text: str) -> str:
        ...


class UpperFormatter(Formatter, name="upper"):
    def format(self, text):
        return text.upper()


class ReverseFormatter(Formatter, name="reverse"):
    def format(self, text):
        return text[::-1]


def apply(name, text):
    return Formatter.registry[name]().format(text)

print(apply("upper", "odyssey"))
print(apply("reverse", "odyssey"))
print(sorted(Formatter.registry))
