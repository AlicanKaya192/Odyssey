`BoundedCache` sınırsız büyüyor. `OrderedDict` ile en fazla `max_size` öğe
tutan bir LRU önbelleğe çevir:

- `put`: ekle, `move_to_end(key)` ile en sona taşı; sınır aşıldıysa en eskiyi
  `popitem(last=False)` ile at.
- `get`: yoksa `None`; varsa en sona taşı ve değeri döndür.

`simulate` hazır; önbellekte kalan anahtarları sırasıyla döndürüyor.

**Beklenen çıktı:**

```
['c', 'a', 'd']
['y', 'z']
```
