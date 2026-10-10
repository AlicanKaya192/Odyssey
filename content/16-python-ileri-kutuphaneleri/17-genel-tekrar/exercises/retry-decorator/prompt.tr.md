`retry(times)` adında bir süsleyici fabrikası yaz:

- Sarılan fonksiyonu en fazla `times` kez dener; `ValueError` gelirse
  `log.warning("retry %d: %s", deneme, hata)` yazar ve yeniden dener.
- Son denemede de hata gelirse hatayı yeniden fırlatır (`raise`).
- `functools.wraps` ile adı korunur.

Beklenen çıktı:

```
ok 3 flaky
WARNING retry 1: try 1
WARNING retry 2: try 2
```

**Beklenen çıktı:**

```
ok 3 flaky
WARNING retry 1: try 1
WARNING retry 2: try 2
```
