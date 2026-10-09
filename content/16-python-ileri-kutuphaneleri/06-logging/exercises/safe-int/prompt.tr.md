`safe_int(text)` metni `int`'e çevirsin; olmazsa (`ValueError`) hatayı
`log.exception("bad number: %s", text)` ile kaydetsin ve `None` döndürsün.
Kaydedicinin işleyicisi hazır: kayıtları `buffer`'a yazıyor.

**Beklenen çıktı:**

```
42 None
ERROR: bad number: 4x
ValueError
```
