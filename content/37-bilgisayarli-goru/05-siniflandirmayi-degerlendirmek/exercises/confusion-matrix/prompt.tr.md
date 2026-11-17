`confusion(y_true, y_pred, k)` `k` sınıflı bir karışıklık matrisini (satır
gerçek, sütun tahmin) iç içe liste olarak döndürsün. Dersteki
`torch.bincount` yolunu kullanabilirsin.

**Beklenen çıktı:**

```
[1, 1, 0]
[0, 2, 0]
[1, 0, 1]
```
