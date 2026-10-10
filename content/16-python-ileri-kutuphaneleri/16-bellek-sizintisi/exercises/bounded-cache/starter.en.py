from collections import OrderedDict


class BoundedCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


def simulate(max_size, keys):
    cache = BoundedCache(max_size)
    for key in keys:
        if cache.get(key) is None:
            cache.put(key, key.upper())
    return list(cache.data)


print(simulate(3, ["a", "b", "c", "a", "d"]))
print(simulate(2, ["x", "y", "z"]))
