`flag_anomalies(errors, train_errors, q)` eşiği eğitim hatalarının `q`
dilimi olarak alsın (`torch.quantile`) ve her hata için eşiği **aşıp
aşmadığını** mantıksal liste olarak döndürsün.

**Beklenen çıktı:**

```
[False, True, True]
[False, True, True]
```
