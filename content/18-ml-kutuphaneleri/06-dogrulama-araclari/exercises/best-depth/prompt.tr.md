`best_depth(depths)` `validation_curve(DecisionTreeClassifier(random_state=0), X, y,
param_name="max_depth", param_range=depths, cv=5)` çalıştırsın ve
`[en_iyi_derinlik, test_ortalamaları]` döndürsün: ortalamalar 3 basamaklı
liste, en iyi derinlik test ortalaması en yüksek olan (eşitlikte ilki).

**Beklenen çıktı:**

```
[4, [0.773, 0.79, 0.82, 0.787]]
```
