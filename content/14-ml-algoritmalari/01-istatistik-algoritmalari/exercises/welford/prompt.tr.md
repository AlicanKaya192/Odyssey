`welford(values)` fonksiyonunu **Welford algoritmasıyla**, listeyi bir kez
gezerek yaz: `(ortalama, varyans)` demetini döndürsün, ikisi de
`round(..., 4)`; varyans `M2 / n`.

Her değerde: `n += 1`, `delta = v − mean`, `mean += delta / n`,
`m2 += delta * (v − mean)`.

**Beklenen çıktı:**

```
(5.0, 4.0)
(10.0, 0.0)
```
