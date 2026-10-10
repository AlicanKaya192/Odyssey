`price(product_id)` sonuçları kendi sözlüğünde saklıyor ve sözlük hiç
küçülmüyor. Sözlüğü kaldır, fonksiyona `@lru_cache(maxsize=256)` ekle.
Beklenen çıktı:

```
256 22
```

**Beklenen çıktı:**

```
256 22
```
