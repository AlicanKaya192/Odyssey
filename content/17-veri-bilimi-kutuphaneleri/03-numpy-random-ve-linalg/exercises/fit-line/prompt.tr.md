`fit_line(xs, ys)` en küçük karelerle `y ≈ a + b x` doğrusunu bulsun ve
`[a, b]`'yi 3 basamağa yuvarlı döndürsün. İlk sütunu 1, ikinci sütunu `xs`
olan bir `X` matrisi kur (`np.column_stack`) ve `np.linalg.lstsq(X, ys,
rcond=None)` kullan.

**Beklenen çıktı:**

```
[0.15, 1.94]
```
