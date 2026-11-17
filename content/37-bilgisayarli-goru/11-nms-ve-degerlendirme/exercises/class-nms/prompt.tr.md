`class_nms(boxes, scores, labels, conf, iou)` önce puanı `conf`'tan küçük
kutuları atsın, sonra `batched_nms` ile sınıf sınıf NMS yapsın. Kalan
kutuların **özgün listedeki** numaralarını (puan sırasıyla) döndürsün.

**Beklenen çıktı:**

```
[0, 3, 2]
[0, 3, 2]
```
