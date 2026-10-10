`pdp_values(column, points)` test verisinde verilen sütunun kısmi
bağımlılık ortalamalarını (`grid_resolution=points`, tam sayıya yuvarlanmış)
döndürsün. Başlangıç kodu `floor` gibi tam sayı sütunda hata alıyor; sütunu
önce `float`'a çevir.

**Beklenen çıktı:**

```
[106, 124, 159, 163, 163]
[118, 158, 157, 115]
```
