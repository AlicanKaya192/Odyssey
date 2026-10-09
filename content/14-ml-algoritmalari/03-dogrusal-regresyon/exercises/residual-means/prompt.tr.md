`residual_means(x, y, parts)` fonksiyonunu yaz: `x`'e göre sırala, doğru
uydur (kesişim + eğim, `lstsq`), artıkları (`y − ŷ`) `np.array_split` ile
`parts` parçaya böl ve her parçanın ortalamasını `round(..., 2)` ile liste
olarak döndürsün.

**Beklenen çıktı:**

```
[3.0, -6.0, 3.0]
```
