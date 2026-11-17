`encode(boxes, S, size, C)` `[x1, y1, x2, y2, sınıf]` kutularından derste
anlatılan `(S, S, 5 + C)` hedef tensörünü kurup `.tolist()` ile
döndürsün: nesnellik, hücre içi merkez, resme oranla genişlik ve yükseklik,
tek-sıcak sınıf.

**Beklenen çıktı:**

```
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[1.0, 0.5, 0.25, 0.5, 0.25, 0.0, 1.0]
[1.0, 0.75, 0.0, 0.5, 0.5, 1.0, 0.0]
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```
