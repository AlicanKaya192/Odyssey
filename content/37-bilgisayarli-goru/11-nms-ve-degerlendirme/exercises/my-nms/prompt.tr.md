`my_nms(boxes, scores, threshold)` NMS'i kendisi yapsın: kutuları puana göre
sırala, en yüksek puanlıyı tut, onunla IoU'su `threshold`'dan büyük olanları
at, kalanlarla devam et. Tutulan kutuların numaralarını tutulma sırasıyla
döndürsün. IoU için `box_iou` kullanabilirsin; `nms` kullanma.

**Beklenen çıktı:**

```
[0, 3]
[4, 1]
[0, 3, 1, 4]
```
