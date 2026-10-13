`pmi(n_pair, n_word, n_context, total)` sayımlardan PMI'ı hesaplasın ve 3
basamakla döndürsün:

- `P(w, c) = n_pair / total`, `P(w) = n_word / total`, `P(c) = n_context / total`
- `PMI = log(P(w, c) / (P(w) · P(c)))` (doğal logaritma)

**Beklenen çıktı:**

```
0.632
-1.023
```
