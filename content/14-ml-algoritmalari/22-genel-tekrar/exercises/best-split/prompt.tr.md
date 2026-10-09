`best_split(x, y)` fonksiyonunu yaz: tek bir sayısal özellik `x`, sınıflar
`y`. Ardışık **farklı** sıralı değerlerin orta noktalarını eşik olarak dene;
`x <= eşik` sol, gerisi sağ. Ağırlıklı Gini safsızlığı en küçük olan eşiği ve
safsızlığı `(eşik, round(gini, 3))` döndürsün; eşitlikte küçük eşik.
`Gini = 1 − Σ pₖ²`.

**Beklenen çıktı:**

```
(3.5, 0.0)
(1.5, 0.333)
```
