`lasso_fit(X, y, alpha, rounds)` fonksiyonunu yaz (scikit-learn ölçeği):
merkezle; `w` sıfırdan; her turda her `j` için
`artık = yc − Xc w + Xc[:, j] w[j]`, `ρ = Xc[:, j] · artık / n`,
`w[j] = soft(ρ, α) / (Xc[:, j] · Xc[:, j] / n)`. `[kesişim, w…]` listesini
`round(..., 3)` ile döndürsün.

`Lasso` yok.

**Beklenen çıktı:**

```
[1.15, 1.95, 0.0, -0.0]
[4.0, 1.0, 0.0, -0.0]
```
