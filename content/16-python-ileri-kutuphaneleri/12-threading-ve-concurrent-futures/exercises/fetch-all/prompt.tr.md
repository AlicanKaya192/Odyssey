`fake_fetch(url)` her çağrıda 0,3 saniye bekliyor. `fetch_all(urls)`
adresleri sırayla çektiği için 10 adres 3 saniye sürüyor. Fonksiyonu
`ThreadPoolExecutor(max_workers=10)` ve `pool.map` ile yeniden yaz; sonuçlar
yine **adres sırasıyla** bir liste olsun. Beklenen çıktı:

```
[22, 22, 22, 22, 22, 22, 22, 22, 22, 22]
True
```

**Beklenen çıktı:**

```
[22, 22, 22, 22, 22, 22, 22, 22, 22, 22]
True
```
