`tuned_threshold(fn_cost)` `cost` ölçüsüyle (`fn_cost` ek ayar olarak
`make_scorer`'a verilir) `TunedThresholdClassifierCV(LogisticRegression(),
scoring=scorer, cv=5)`'i eğitim verisinde eğitsin ve `[eşik, test_maliyeti]`
döndürsün: eşik `best_threshold_` 3 basamak, maliyet ayarlı modelin test
tahminlerinden.

**Beklenen çıktı:**

```
[0.455, 4]
[0.293, 43]
```
