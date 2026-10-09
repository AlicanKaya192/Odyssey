`stratified_test(y, test_size, seed)` fonksiyonunu yaz: `rng =
np.random.default_rng(seed)`; `np.unique(y)` sırasıyla her sınıfın indekslerini
`rng.permutation` ile karıştır ve ilk `round(len * test_size)` tanesini teste
al. Test indekslerini **sıralı** liste olarak döndürsün.

**Beklenen çıktı:**

```
[2, 4, 5, 7, 8]
```
