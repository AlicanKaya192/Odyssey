`times` küçükten büyüğe sıralı başarısızlık saniyeleri.
`window_alerts(times, window, limit)` her yeni olaydan sonra son
`window` saniyedeki olayları say (`t - window`'dan **büyük** olanlar) ve
sayı `limit`'e ulaştıysa o olayın saniyesini listeye ekle. Listeyi
döndür.

**Beklenen çıktı:**

```
[31, 44, 220]
[]
```
