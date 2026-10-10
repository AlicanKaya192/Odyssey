`top_growth(func)` fonksiyonunu yaz:

- `tracemalloc.start()`, bir fotoğraf al, `func()`'ı çağır, ikinci fotoğrafı
  al.
- `compare_to(önceki, "lineno")` ile karşılaştır, ilk sıradaki istatistiğin
  `traceback[0]` çerçevesini al.
- O satırın **kaynak metnini** `linecache.getline(dosya, satır).strip()`
  ile döndür ve `tracemalloc.stop()` yap.

**Beklenen çıktı:**

```
kept.append(bytearray(1_000))
```
