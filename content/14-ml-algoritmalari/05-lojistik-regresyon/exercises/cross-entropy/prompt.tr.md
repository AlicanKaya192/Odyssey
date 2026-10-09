`cross_entropy(y, p)` fonksiyonunu yaz: log kaybı
`−ort(y log p + (1 − y) log(1 − p))`. `log(0)` olmasın diye önce
`p = np.clip(p, 1e-12, 1 - 1e-12)`. `round(..., 4)` döndürsün.

`log_loss` yok.

**Beklenen çıktı:**

```
0.2798
4.6052
0.0
```
