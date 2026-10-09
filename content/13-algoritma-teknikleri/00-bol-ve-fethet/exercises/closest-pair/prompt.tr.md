`closest(points)` fonksiyonunu **böl ve fethet** ile yaz: `x`'e göre sıralı
noktaların en yakın çiftinin uzaklığını döndürsün.

1. En fazla 3 nokta: bütün çiftlere bak (`math.dist`).
2. Ortadan böl (`mid_x = points[mid][0]`), iki yarıyı çöz, küçüğü `d`.
3. `abs(x - mid_x) < d` olanları `y`'ye göre sırala; her nokta için
   sonrakilere bak, `y` farkı `d`'yi geçince dur.

`closest_distance` sıralayıp sonucu yuvarlıyor. Son satırdaki 30 000 nokta
kaba kuvveti (450 milyon uzaklık) süre sınırına takar.

**Beklenen çıktı:**

```
1.0
28.79236
```
