`first_occurrence(items, target)` fonksiyonunu yaz: sıralı ve tekrar
içerebilen bir listede `target`'ın **ilk** geçtiği indeksi ikili aramayla
bulsun; yoksa `-1`.

- `[1, 3, 3, 3, 5]` içinde `3` → `1`

Eşleşmeyi bulunca hemen durma: cevabı not et (`answer = mid`) ve **solda**
aramaya devam et (`hi = mid - 1`).

**Kurallar:** `.index()` ve `bisect` kullanma.

**Beklenen çıktı:**

```
1
4
-1
```
