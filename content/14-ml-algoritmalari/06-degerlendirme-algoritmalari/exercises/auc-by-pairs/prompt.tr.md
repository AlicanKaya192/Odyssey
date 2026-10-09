`auc_by_pairs(y, score)` fonksiyonunu yaz: bütün (pozitif, negatif)
çiftlerinde pozitifin puanı büyükse 1, eşitse 0,5, küçükse 0 say; ortalamayı
`round(..., 4)` ile döndürsün. Bu, ROC AUC'nin kendisidir.

`roc_auc_score` yok.

**Beklenen çıktı:**

```
0.75
0.5
```
