`random_forest_search(n_iter)` eğitim verisinde
`RandomizedSearchCV(RandomForestClassifier(min_samples_leaf=10, random_state=0),
uzay, n_iter=n_iter, cv=3, random_state=0)` çalıştırsın. Uzay: `"n_estimators": randint(10, 60)`,
`"max_depth": randint(2, 8)`. `[en_iyi_max_depth, en_iyi_skor]` döndürsün
(derinlik `int`, skor 3 basamak).

`min_samples_leaf=10` yaprakları büyük tutuyor: çok küçük yapraklarda iki
ayrım tam eşit puan alabiliyor ve bu eşitlik işlemciye göre farklı bozuluyor;
büyük yapraklarla sonuç her bilgisayarda aynı.

**Beklenen çıktı:**

```
[5, np.float64(0.8)]
```
