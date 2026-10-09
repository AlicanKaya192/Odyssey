In the lesson we wrote the LRU cache with `OrderedDict`. To see what is
inside, let us build the same thing by hand with **a dictionary + a doubly
linked list**. The front of the list is the least recently used, the end the
most recently used; there is a **sentinel** node at both ends so that an empty
list needs no separate code.

```python
class DNode:
    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}                          # key → node
        self.head, self.tail = DNode(), DNode()  # sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node):                     # add at the end (newest)
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        node = self.nodes.get(key)
        if node is None:
            return None
        self._unlink(node)
        self._append(node)                       # make it the newest
        return node.value

    def put(self, key, value):
        if key in self.nodes:
            self._unlink(self.nodes[key])
        node = DNode(key, value)
        self.nodes[key] = node
        self._append(node)
        if len(self.nodes) > self.capacity:
            oldest = self.head.next              # the oldest at the front
            self._unlink(oldest)
            del self.nodes[oldest.key]

cache = LRU(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.put("c", 3)
print(cache.get("b"), cache.get("a"), cache.get("c"))   # None 1 3
```

Every operation is a few link changes and one dictionary operation: all
`O(1)`.

**Why does the node keep the key too?** When the oldest is dropped from the
list it must also be deleted from the dictionary; the node tells which key it
is stored under.
