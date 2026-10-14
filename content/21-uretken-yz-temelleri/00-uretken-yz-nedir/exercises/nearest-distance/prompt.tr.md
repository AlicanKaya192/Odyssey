`nearest_distances(points, name)` verilen her balığın, `name` türünün gerçek
balıkları arasındaki en yakın komşusuna uzaklığını döndürsün. Uzaklıktan
önce boyu ve ağırlığı türün standart sapmasına (`part.std(axis=0)`) böl.
Sonuç 3 basamağa yuvarlanmış liste olsun. Gerçek bir balığın kendisi için
uzaklık 0 çıkmalı.

**Beklenen çıktı:**

```
[0.0, 0.012, 1.657]
```
