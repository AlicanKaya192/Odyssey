`iou(a, b)` iki xyxy kutunun IoU'sunu 3 basamakla döndürsün. Ortak bölgenin
genişliği ve yüksekliği eksi çıkarsa 0 say. torchvision'ın `box_iou`'sunu
kullanma.

**Beklenen çıktı:**

```
[10, 10, 20, 20] 1.0
[15, 10, 25, 20] 0.333
[12, 12, 22, 22] 0.471
[30, 30, 40, 40] 0.0
[0, 0, 10, 10] 0.0
```
