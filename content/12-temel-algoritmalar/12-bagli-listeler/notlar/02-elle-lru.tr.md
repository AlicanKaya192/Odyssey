Derste LRU önbelleği `OrderedDict` ile yazdık. İçinde ne olduğunu görmek
için aynısını **sözlük + çift yönlü bağlı liste** ile elle kuralım. Listenin
başı en eski, sonu en yeni kullanılan; iki uçta da **nöbetçi** düğüm var ki
boş liste için ayrı kod gerekmesin.

```python
class DNode:
    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}                          # anahtar → düğüm
        self.head, self.tail = DNode(), DNode()  # nöbetçiler
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node):                     # sona (en yeni) ekle
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        node = self.nodes.get(key)
        if node is None:
            return None
        self._unlink(node)
        self._append(node)                       # en yeni yap
        return node.value

    def put(self, key, value):
        if key in self.nodes:
            self._unlink(self.nodes[key])
        node = DNode(key, value)
        self.nodes[key] = node
        self._append(node)
        if len(self.nodes) > self.capacity:
            oldest = self.head.next              # baştaki en eski
            self._unlink(oldest)
            del self.nodes[oldest.key]

cache = LRU(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.put("c", 3)
print(cache.get("b"), cache.get("a"), cache.get("c"))   # None 1 3
```

Her işlem birkaç bağlantı değişikliği ve bir sözlük işlemi: hepsi `O(1)`.

**Neden düğüm anahtarı da tutuyor?** En eskiyi listeden atınca sözlükten de
silmek gerekiyor; sözlükte hangi anahtarla durduğunu düğüm söylüyor.
