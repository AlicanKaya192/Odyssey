`forward_pass(X, W1, b1, W2, b2)` fonksiyonunu yaz: `H = tanh(X W₁ + b₁)`,
`p = σ(H W₂ + b₂)`; `p`'yi tek boyutlu liste olarak (`.ravel()`)
`.round(3).tolist()` ile döndürsün.

**Beklenen çıktı:**

```
[0.525, 0.681, 0.868]
```
