Modeller her zaman bir **küme** bekler: tek bir gri görüntüyü (yükseklik ×
genişlik) bile `(1, 1, yükseklik, genişlik)` şeklinde verirsin. `batch_of_one(image)`
iki boyutlu tensörün başına iki boyut eklesin ve yeni şekli liste olarak
döndürsün.

**Beklenen çıktı:**

```
[1, 1, 2, 3]
```
