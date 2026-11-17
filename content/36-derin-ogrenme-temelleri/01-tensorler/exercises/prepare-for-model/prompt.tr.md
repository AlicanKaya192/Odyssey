`prepare(rows, labels)` girdileri NumPy üzerinden tensöre çeviriyor ama
türler yanlış: modelin istediği girdi `float32`, etiket `int64`. Fonksiyonu
düzelt; `[girdi türü, etiket türü, girdi şekli]` döndürsün.

**Beklenen çıktı:**

```
['torch.float32', 'torch.int64', [3, 2]]
```
