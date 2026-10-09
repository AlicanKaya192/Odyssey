`momentum_fit(A, y, lr, beta, steps)` fonksiyonunu yaz: `w` ve `v` sıfırdan
başlar; her adımda `v = beta · v + gradyan`, `w = w − lr · v` (MSE gradyanı).
Son ağırlıkları `.round(3).tolist()` ile döndürsün. `beta = 0` düz gradyan
inişidir.

**Beklenen çıktı:**

```
[0.971, 2.013]
[1.045, 2.094]
```
