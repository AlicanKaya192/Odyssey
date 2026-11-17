`trace_shapes(sizes, batch)` sıfırlardan oluşan bir girdiyi `build(sizes)`
modelinin katmanlarından tek tek geçirsin ve her katman için
`[katmanın sınıf adı, çıktı şekli listesi]` eklesin.

**Beklenen çıktı:**

```
['Linear', [3, 4]]
['ReLU', [3, 4]]
['Linear', [3, 2]]
```
