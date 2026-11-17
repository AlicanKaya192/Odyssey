`match_counts(predicted, truth, threshold)` tahminleri (`[x1, y1, x2, y2,
sınıf, güven]`) güvene göre büyükten küçüğe dolaşıp her birini aynı sınıftan,
henüz eşleşmemiş ve IoU'su en yüksek gerçek kutuyla (`[x1, y1, x2, y2,
sınıf]`) eşleştirsin. IoU eşikten küçük değilse doğru pozitif, yoksa yanlış
pozitif. `[TP, FP, FN]` döndür. Hazır `iou` fonksiyonunu kullan.

**Beklenen çıktı:**

```
[1, 2, 1]
```
