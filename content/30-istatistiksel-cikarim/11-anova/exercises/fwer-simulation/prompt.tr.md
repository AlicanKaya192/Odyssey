`fwer(k, n, reps, seed)` hepsi aynı olan `k` grubun (her biri `n` değer,
`rng.normal(0, 1, size=(k, n))`) bütün çiftlerini `ttest_ind` ile
karşılaştırsın ve `reps` tekrarda **en az bir** çiftin `p < 0.05` çıktığı
payı 3 basamakla döndürsün. Başlangıç kodu yalnızca ilk çifte bakıyor.

**Beklenen çıktı:**

```text
0.222
0.046
```
