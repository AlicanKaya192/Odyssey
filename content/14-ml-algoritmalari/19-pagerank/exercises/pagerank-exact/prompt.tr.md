`pagerank_exact(M, d)` fonksiyonunu yaz: `(I − d M) r = (1 − d) / n`
denklemini `np.linalg.solve` ile çöz; `r`'yi `.round(3).tolist()` ile
döndürsün. Döngü yok.

**Beklenen çıktı:**

```
[0.388, 0.215, 0.397]
[0.359, 0.256, 0.385]
```
