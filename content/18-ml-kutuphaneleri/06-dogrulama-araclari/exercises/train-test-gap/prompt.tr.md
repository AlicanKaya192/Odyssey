`train_test_gap(depth)` `DecisionTreeClassifier(max_depth=depth, random_state=0)`
için `cross_validate(..., cv=5, scoring=["accuracy", "f1"],
return_train_score=True)` çalıştırsın ve 3 basamakla şunu döndürsün:

- `"train"`: eğitim doğruluğu ortalaması
- `"test"`: test doğruluğu ortalaması
- `"f1"`: test F1 ortalaması

**Beklenen çıktı:**

```
{'train': 1.0, 'test': 0.78, 'f1': 0.488}
{'train': 0.87, 'test': 0.81, 'f1': 0.429}
```
