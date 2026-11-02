`sample_mean(values, n, seed)` `values` listesinden **tekrarsız** `n` değer
seçip ortalamasını 2 basamakla döndürsün. Seçim için
`np.random.default_rng(seed).choice(values, size=n, replace=False)`.
Başlangıç kodu bütün listenin ortalamasını (parametreyi) döndürüyor;
örneklemin ortalaması (istatistik) isteniyor.

**Beklenen çıktı:**

```text
9.6
10.2
10.5
```
