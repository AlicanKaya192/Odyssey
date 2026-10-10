`best_pruned(folds)` sınırsız ağacın `cost_complexity_pruning_path`'inden
`ccp_alphas` adaylarını alsın, `GridSearchCV(..., cv=folds)` ile en iyisini
seçsin ve `[alpha, yaprak_sayısı, test_skoru]` döndürsün (alpha 4, skor 3
basamak; ağaçlarda `random_state=0`). Başlangıç kodu budamıyor.

**Beklenen çıktı:**

```
[0.0062, 12, 0.9]
[0.0088, 9, 0.867]
```
