`pagerank(links, d=0.85, tol=1e-10)` fonksiyonunu yaz (`links[j]`: `j`'nin
bağlantıları): geçiş matrisini kur (çıkmaz sayfanın sütunu `1 / n`),
`1 / n`'den başla ve adımı `Σ abs(yeni − eski) < tol` olana kadar tekrarla.
`(sıralar round(3) liste, adım sayısı)` döndürsün; adım sayısı yapılan
güncelleme sayısı.

**Beklenen çıktı:**

```
[0.373, 0.196, 0.394, 0.038]
47
```
