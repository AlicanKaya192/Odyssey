`pegasos_step(x, yi, w, b, lam, t)` fonksiyonunu yaz: `lr = 1 / (lam · t)`.
`yi (x·w + b) < 1` ise `w = (1 − lr·lam) w + lr·yi·x` ve `b += lr·yi`; değilse
yalnızca `w = (1 − lr·lam) w`. `(w listesi, b)` demetini, değerler
`round(..., 4)` olarak döndürsün.

**Beklenen çıktı:**

```
[10.0, 20.0] 10.0
[5.0, 10.0] 10.0
```
