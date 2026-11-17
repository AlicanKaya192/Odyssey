`count_tp_fp_fn(pred_boxes, pred_scores, truth_boxes, threshold)` açgözlü
eşleştirme yapsın: tahminleri puan sırasıyla gez; her biri henüz
eşleşmemiş gerçek kutular arasında IoU'su en yüksek olanı, IoU ≥
`threshold` ise alsın. `[TP, FP, FN]` döndürsün.

**Beklenen çıktı:**

```
[2, 3, 1]
[2, 0, 1]
```
