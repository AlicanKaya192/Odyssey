`model_auc(kind)` `"linear"` için lojistik pipeline'ın, `"boosting"` için
`HistGradientBoostingClassifier(random_state=0)`'un aynı katlardaki
ortalama AUC'sini (3 basamak) döndürsün. Boosting'de ölçek ve doldurma
gerekmez; yalnızca plan sütunu `OrdinalEncoder` ile sayıya çevrilir
(`ColumnTransformer([("cat", OrdinalEncoder(), ["plan"])],
remainder="passthrough")`). Başlangıç kodu iki durumda da lojistik
kullanıyor.

**Beklenen çıktı:**

```
0.777
0.72
```
