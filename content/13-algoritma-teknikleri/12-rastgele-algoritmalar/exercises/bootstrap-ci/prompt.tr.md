`bootstrap_ci(values, reps, seed)` fonksiyonunu yaz: ortalamanın %95
bootstrap aralığını `(alt, üst)` demeti olarak döndürsün. Üreteç
`rng = random.Random(seed)`.

`reps` kez: `rng.choices(values, k=len(values))` ile yerine koyarak örnek al,
ortalamasını (`sum / len`) listeye ekle. Listeyi sırala;
`alt = means[int(0.025 * reps)]`, `üst = means[int(0.975 * reps)]`, ikisi de
`round(..., 2)`.

**Beklenen çıktı:**

```
(74.3, 85.8)
(5.0, 5.0)
```
