`bm25(query)` her makale için BM25 puanını hesaplayıp bir liste döndürsün.
Her sorgu kelimesi `w` makalede geçiyorsa:

- `idf = log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))`
- `norm = k1 * (1 - b + b * len(doc) / avg_len)`
- puana `idf * tf[w] * (k1 + 1) / (tf[w] + norm)` eklenir

`tokens`, `df`, `avg_len`, `N` ve `analyze` hazır.

**Beklenen çıktı:**

```
9.441
Tracking your order
4.565
Resetting your password
```
