`clusters(points, k)` fonksiyonunu yaz: noktaları **tek bağlantılı
kümeleme** ile `k` gruba ayırsın. Bütün nokta çiftlerini uzaklığa göre sırala
(`math.dist`), birleşim-bulma ile birleştir; grup sayısı `k`'ya inince dur.

Dönüş: her grup noktaların **indekslerinin** sıralı listesi, gruplar da ilk
indekslerine göre sıralı.

**Beklenen çıktı:**

```
[0, 1, 2]
[3, 4, 7]
[5, 6]
[[0, 1, 2, 3, 4, 5, 6, 7]]
```
