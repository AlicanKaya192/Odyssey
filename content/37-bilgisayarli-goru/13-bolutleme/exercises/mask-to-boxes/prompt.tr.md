`mask_boxes(mask)` maskedeki her sınıf (1 ve üstü) için o sınıfın bütün
piksellerini içine alan kutuyu `[x1, y1, x2, y2, sınıf]` olarak, sınıf
sırasıyla döndürsün. `x2` ve `y2` dahil değil (en büyük + 1). Maskede
olmayan sınıfı atla.

**Beklenen çıktı:**

```
[0, 3, 1, 4, 1]
[1, 1, 3, 3, 2]
[4, 2, 5, 4, 3]
```
