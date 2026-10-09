`tree_predict(tree, X)` fonksiyonunu yaz: ağaç iç içe sözlük; iç düğüm
`{"feature", "threshold", "left", "right"}`, yaprak `{"leaf"}`. Her satır için
kökten başla: `x[feature] <= threshold` ise sola, değilse sağa; yaprağa gelince
değeri al. Etiket listesini döndürsün.

**Beklenen çıktı:**

```
[0, 1, 0]
```
