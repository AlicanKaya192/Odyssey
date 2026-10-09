`cm_estimates(stream, queries, width, depth)` fonksiyonunu yaz: `depth`
satır, `width` sütunluk bir Count-Min tablosu kur; akıştaki her öğe için her
satırda (`row`) `h(item, row) % width` sütununu bir artır. Her sorgu için
tahmini (satırlardaki sayaçların en küçüğü) liste olarak döndürsün.

**Beklenen çıktı:**

```
[56, 25, 5, 4]
```
