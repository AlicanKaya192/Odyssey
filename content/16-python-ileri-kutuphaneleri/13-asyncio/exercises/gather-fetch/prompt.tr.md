`fetch_all(names)` her adı sırayla `await fetch(name)` ile çekiyor; beş ad
1 saniye sürüyor. `asyncio.gather` ile hepsini birlikte beklet; sonuçlar yine
**ad sırasıyla** liste olsun. Alttaki `run_fetch_all` sarmalayıcısını
değiştirme. Beklenen çıktı:

```
[1, 2, 3, 4, 1]
True
```

**Beklenen çıktı:**

```
[1, 2, 3, 4, 1]
True
```
