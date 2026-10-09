`permutation_p(a, b, rounds, seed)` fonksiyonunu yaz: iki grubun ortalama
farkının mutlak değeri gerçek istatistik. `rng =
np.random.default_rng(seed)`; `rounds` kez birleşik veriyi `rng.permutation`
ile karıştır, ilk `len(a)` tanesini a, kalanını b say ve farkı hesapla. p
değeri `(gerçekten büyük ya da eşit olanlar + 1) / (rounds + 1)`,
`round(..., 4)`.

**Beklenen çıktı:**

```
0.022
1.0
```
