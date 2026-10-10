`pipe_search(ks, cs)` `make_pipeline(StandardScaler(), SelectKBest(f_classif),
LogisticRegression())` üzerinde `k` ve `C`'yi birlikte arasın (`cv=5`,
eğitim verisinde). Izgara anahtarları `adım__ayar` biçiminde olmalı. Şunu
döndürsün:

- `"params"`: `[en_iyi_k, en_iyi_C]`
- `"test"`: en iyi modelin test skoru, 3 basamak

Başlangıç kodu anahtarları `"k"` ve `"C"` yazıyor ve hata veriyor.

**Beklenen çıktı:**

```
[8, 0.1]
0.893
```
