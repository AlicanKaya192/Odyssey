`backprop_w1(X, y, W1, b1, W2, b2)` fonksiyonunu yaz: ileri yayılımı yap
(`tanh` gizli, sigmoid çıkış), sonra `dz₂ = (p − y) / n`,
`dz₁ = (dz₂ W₂ᵀ) · (1 − H²)`, `dW₁ = Xᵀ dz₁`. `dW₁`'i `.round(4).tolist()`
ile döndürsün.

**Beklenen çıktı:**

```
[0.0359, -0.1061]
[-0.0703, -0.0703]
```
