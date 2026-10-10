from collections import OrderedDict


class BoundedCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.data = OrderedDict()

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.max_size:
            self.data.popitem(last=False)

    def get(self, key):
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]


def simulate(max_size, keys):
    cache = BoundedCache(max_size)
    for key in keys:
        if cache.get(key) is None:
            cache.put(key, key.upper())
    return list(cache.data)


print(simulate(3, ["a", "b", "c", "a", "d"]))
print(simulate(2, ["x", "y", "z"]))
