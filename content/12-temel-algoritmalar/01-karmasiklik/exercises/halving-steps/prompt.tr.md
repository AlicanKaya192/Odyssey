`halving_steps(n)` fonksiyonunu yaz: `n` 1'den büyük olduğu sürece `n`'yi
tam sayı bölmesiyle ikiye bölsün (`n //= 2`) ve kaç kez böldüğünü
döndürsün. `n` 1 ise `0` döner.

`math.log` kullanma; amaç logaritmayı döngüyle görmek.

Sonra 1, 2, 8, 1000 ve 1 000 000 için `n`'yi ve sonucu yazdır.

**Beklenen çıktı:**

```
1 0
2 1
8 3
1000 9
1000000 19
```

Bir milyon için yalnızca 19 adım: `O(log n)`.
