`idf(df, n)` scikit-learn'ün varsayılan formülüyle IDF'i hesaplayıp 3
basamağa yuvarlasın: `ln((1 + n) / (1 + df)) + 1`. `math.log` doğal
logaritma.

**Beklenen çıktı:**

```
1 7.216
10 5.511
100 3.294
1000 1.0
```
