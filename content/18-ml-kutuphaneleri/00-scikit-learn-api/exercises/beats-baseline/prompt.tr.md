`beats_baseline(weight)` `make_classification(n_samples=1000, n_features=5,
weights=[weight], random_state=3)` ile dengesiz bir veri üretsin,
`train_test_split(..., random_state=3)` ile bölsün ve iki model eğitsin:
`DummyClassifier(strategy="most_frequent")` ve `LogisticRegression()`.
Şunu döndürsün:

- `"baseline"`, `"model"`: test doğrulukları, 3 basamak
- `"better"`: modelin doğruluğu taban çizgisinden **en az 0.02** yüksek mi

**Beklenen çıktı:**

```
0.892 0.94
True
```
