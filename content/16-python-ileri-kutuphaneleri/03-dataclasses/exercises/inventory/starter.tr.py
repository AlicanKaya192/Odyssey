from dataclasses import dataclass, field

SHARED = {}


@dataclass
class Inventory:
    owner: str
    items: dict[str, int] = field(default_factory=lambda: SHARED)

    def add(self, name, count):
        self.items[name] = self.items.get(name, 0) + count

a = Inventory("ada")
b = Inventory("alan")
a.add("pen", 3)
a.add("pen", 2)
print(a)
print(b)
