`skewed_fit(seed)` üstel büyüyen bir hedef üretiyor ve bölüyor. Modeli
`TransformedTargetRegressor(regressor=LinearRegression(), func=np.log,
inverse_func=np.exp)` yap ve `[test_R2, x=0_tahmini]` döndür (2'şer basamak).
Başlangıç kodu düz `LinearRegression` kullanıyor.

**Beklenen çıktı:**

```
[0.81, 2.66]
```
