`filter_detections(xyxy, conf, cls, wanted, min_conf, iou)` bir algılama
kütüphanesinin çıktısından yalnızca `wanted` sınıfındaki ve güveni
`min_conf`'tan küçük olmayan kutuları tutsun, onlara `nms` uygulasın ve
kalan kutuları liste olarak döndürsün.

**Beklenen çıktı:**

```
0 0.5 1
[10.0, 10.0, 30.0, 60.0]
0 0.3 2
[10.0, 10.0, 30.0, 60.0]
[100.0, 5.0, 120.0, 55.0]
2 0.5 1
[50.0, 20.0, 90.0, 45.0]
```
