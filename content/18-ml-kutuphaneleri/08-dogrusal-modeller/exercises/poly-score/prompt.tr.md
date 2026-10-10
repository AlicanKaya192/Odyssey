`poly_score(degree)` modelin başına `PolynomialFeatures(degree)` eklesin
(`PolynomialFeatures` → `StandardScaler` → `Ridge(alpha=1e-3)`) ve verilen
`KFold` ile ortalama R²'yi 3 basamakla döndürsün. Başlangıç kodunda
`degree` hiç kullanılmıyor.

**Beklenen çıktı:**

```
0.641
0.963
```
