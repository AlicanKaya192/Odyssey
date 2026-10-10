import weakref


class Registry:
    def __init__(self):
        self.items = weakref.WeakSet()

    def add(self, item):
        self.items.add(item)

    def count(self):
        return len(self.items)

class Item:
    pass


registry = Registry()
items = [Item() for _ in range(3)]
for item in items:
    registry.add(item)
del item  # the loop variable is a reference too
print(registry.count())
del items[0]
print(registry.count())
items.clear()
print(registry.count())
