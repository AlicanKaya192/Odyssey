`prf(y_true, y_pred, label)` verilen sınıf için `[kesinlik, duyarlılık, F1]`
listesini (3 basamak) döndürsün. Payda 0 olursa o ölçü `0.0` olsun:

- kesinlik = doğru tahmin / o sınıf denenlerin hepsi
- duyarlılık = doğru tahmin / gerçekte o sınıf olanların hepsi
- F1 = 2PR / (P + R)

**Beklenen çıktı:**

```
[0.5, 0.333, 0.4]
[0.6, 0.75, 0.667]
```
