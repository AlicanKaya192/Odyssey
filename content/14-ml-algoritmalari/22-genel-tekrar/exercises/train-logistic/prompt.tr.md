`train_logistic(X, y, lr, epochs)` fonksiyonunu yaz: `w = 0`, `b = 0`'dan
başla; her dönemde `p = σ(X w + b)`, `w ← w − lr · Xᵀ(p − y) / n`,
`b ← b − lr · ort(p − y)`. `(w listesi round(3), round(b, 3))` döndürsün.

**Beklenen çıktı:**

```
[-0.422, 5.887]
-2.517
```
