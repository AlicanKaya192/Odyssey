`result_shape(shape_a, shape_b)` verilen şekillerde iki sıfır tensörü
(`torch.zeros`) toplasın ve sonucun şeklini liste olarak döndürsün. Şekiller
yayınlanamıyorsa (`RuntimeError`) `"error"` döndürsün.

**Beklenen çıktı:**

```
[3, 2]
[3, 4]
error
```
