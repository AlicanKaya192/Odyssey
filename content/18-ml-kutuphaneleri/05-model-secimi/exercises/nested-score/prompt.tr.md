`nested(cs)` **bütün** veride (`X`, `y`) iki sayı hesaplasın:

- `"inner"`: `GridSearchCV(LogisticRegression(), {"C": cs}, cv=5)`'in
  `best_score_`'u
- `"outer"`: aynı aramanın `cross_val_score(..., cv=5)` ortalaması (iç içe)

İkisi de 3 basamak. `inner` iyimser, `outer` dürüst tahmindir.

**Beklenen çıktı:**

```
0.847 0.847
```
