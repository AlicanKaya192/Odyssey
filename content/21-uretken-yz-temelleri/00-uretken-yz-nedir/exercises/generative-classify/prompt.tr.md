`classify(length, weight)` balığın türünü üretken yolla bulsun. Her tür için
bütün balıklardan ortalama ve kovaryans hesapla, türün oranını (`np.mean(y ==
name)`) bul ve `log_density(...) + np.log(oran)` puanı büyük olan türün adını
döndür. `log_density` hazır verildi.

**Beklenen çıktı:**

```
22 250 perch
33 620 bream
27 420 bream
29 380 perch
```
