`random_forest_search(n_iter)` eğitim verisinde
`RandomizedSearchCV(RandomForestClassifier(random_state=0), uzay, n_iter=n_iter,
cv=3, random_state=0)` çalıştırsın. Uzay: `"n_estimators": randint(10, 60)`,
`"max_depth": randint(2, 8)`. `[en_iyi_max_depth, en_iyi_skor]` döndürsün
(derinlik `int`, skor 3 basamak).

**Beklenen çıktı:**

```
[7, np.float64(0.84)]
```
