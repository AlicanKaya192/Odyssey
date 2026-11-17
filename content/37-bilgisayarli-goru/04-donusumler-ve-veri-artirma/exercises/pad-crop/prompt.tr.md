`pad_crop(img, padding, top, left)` `RandomCrop`'un yaptığını rastgelelik
olmadan yapsın: resmin her yanına `padding` kadar sıfır eklesin
(`F.pad`), sonra `(top, left)` köşesinden başlayan, resimle aynı boyda bir
parça kessin. Sonuç iç içe liste.

**Beklenen çıktı:**

```
[[0, 0], [0, 1]]
[[1, 2], [3, 4]]
[[4, 0], [0, 0]]
```
