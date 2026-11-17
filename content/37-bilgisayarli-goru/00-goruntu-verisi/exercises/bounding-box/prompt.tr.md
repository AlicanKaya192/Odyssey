`bounding_box(img, threshold)` 2B bir resimde (`(H, W)` iç içe liste) değeri
`threshold`'dan büyük piksellerin çevresindeki kutuyu `[x1, y1, x2, y2]`
olarak döndürsün: `x` sütun, `y` satır; `x2` ve `y2` kutuya **dahil
değil** (en büyük + 1). Böyle bir piksel yoksa boş liste. Program
`make_shapes`'in ilk üç resminde dener.

**Beklenen çıktı:**

```
triangle [5, 8, 11, 15]
square [4, 8, 10, 14]
triangle [3, 3, 11, 11]
```
