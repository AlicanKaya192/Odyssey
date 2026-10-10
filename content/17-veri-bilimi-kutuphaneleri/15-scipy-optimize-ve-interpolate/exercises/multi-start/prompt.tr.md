`bumpy` fonksiyonunun birden fazla çukuru var. `multi_start(starts)` her başlangıç
noktasından `optimize.minimize(bumpy, x0=[s])` çalıştırsın ve **en küçük**
değeri veren sonucu seçsin. `[x, değer]` döndürsün (3'er basamak). Başlangıç
kodu yalnızca ilk noktayı deniyor.

**Beklenen çıktı:**

```
[-0.512, -0.973]
[1.537, -0.759]
```
