`delay_after(failures, start, cap)` başarısız deneme sayısı `start`'tan
küçükse `0`, değilse `2 ** (failures - start)` saniye döndürsün; ama
`cap`'i asla geçmesin.

**Beklenen çıktı:**

```
[0, 0, 1, 2, 4, 8, 16]
300
```
