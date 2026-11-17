`nms_by_hand(boxes, scores, threshold)` xyxy kutulara NMS uygulayıp tutulan
kutuların sıralarını, puan sırasıyla (büyükten küçüğe) döndürsün: bir kutu,
tutulan her kutuyla IoU'su eşikten büyük değilse tutulur. torchvision'ın
`nms`'ini kullanma; IoU'yu kendin hesapla.

**Beklenen çıktı:**

```
[3, 2]
[3, 0, 1, 2]
```
