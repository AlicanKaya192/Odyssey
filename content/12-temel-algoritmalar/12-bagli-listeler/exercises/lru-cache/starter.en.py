from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        pass

    def put(self, key, value):
        pass


cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))
cache.put("c", 3)
print(cache.get("b"), cache.get("a"), cache.get("c"))
