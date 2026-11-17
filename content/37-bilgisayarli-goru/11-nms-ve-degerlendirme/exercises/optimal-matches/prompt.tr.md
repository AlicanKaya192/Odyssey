`optimal_matches(predicted, truth, threshold)` `box_iou` ve
`linear_sum_assignment` ile toplam IoU'yu en büyük yapan eşleştirmeyi
bulsun; IoU'su `threshold`'dan küçük olmayan çiftleri `[tahmin, gerçek]`
olarak sıralı bir liste hâlinde döndürsün.

**Beklenen çıktı:**

```
[[0, 0], [1, 1]]
[[1, 0], [2, 1]]
```
