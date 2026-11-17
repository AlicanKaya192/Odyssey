`best_matches(predicted, truth)` `box_iou` ile her tahminin IoU'su en yüksek
gerçek kutusunu bulsun: her tahmin için `[gerçek kutu numarası, IoU]`
(IoU 2 basamak). Hiçbir gerçek kutuyla örtüşmeyen tahminde numara `-1`.

**Beklenen çıktı:**

```
[0, 0.82]
[1, 0.61]
[-1, 0.0]
```
