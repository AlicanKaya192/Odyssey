`split_indices(n, test_size, seed)` fonksiyonunu yaz:
`np.random.default_rng(seed).permutation(n)` ile indeksleri karıştır; ilk
`int(n * test_size)` tanesi test, kalanı eğitim. `(eğitim, test)` demetini
liste olarak döndürsün (`.tolist()`).

**Beklenen çıktı:**

```
[0, 1, 2, 5, 9, 6, 3]
[8, 4, 7]
```
