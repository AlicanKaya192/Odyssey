`bloom_size(n, p)` fonksiyonunu yaz: `n` öğe ve `p` yanlış pozitif oranı için
`(m, k)` demetini döndürsün:

- `m = math.ceil(-n * math.log(p) / math.log(2) ** 2)`
- `k = round(m / n * math.log(2))`

**Beklenen çıktı:**

```
(9585059, 7)
(143776, 10)
```
