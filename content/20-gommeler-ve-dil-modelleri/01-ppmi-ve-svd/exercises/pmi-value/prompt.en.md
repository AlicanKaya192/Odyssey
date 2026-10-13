`pmi(n_pair, n_word, n_context, total)` should compute PMI from counts and
return it with 3 places:

- `P(w, c) = n_pair / total`, `P(w) = n_word / total`, `P(c) = n_context / total`
- `PMI = log(P(w, c) / (P(w) · P(c)))` (natural logarithm)

**Expected output:**

```
0.632
-1.023
```
