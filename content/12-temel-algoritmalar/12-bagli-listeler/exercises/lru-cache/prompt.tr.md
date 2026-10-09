`LRUCache` sınıfını `collections.OrderedDict` ile yaz:

- `LRUCache(capacity)`: en fazla `capacity` anahtar tutar.
- `get(key)`: değeri döndürür (yoksa `None`) ve anahtarı **en yeni** yapar.
- `put(key, value)`: değeri yazar, anahtarı en yeni yapar; kapasite aşıldıysa
  **en eskiyi** atar.

`move_to_end(key)` en yeni yapar, `popitem(last=False)` en eskiyi atar.

**Beklenen çıktı:**

```
1
None 1 3
```
