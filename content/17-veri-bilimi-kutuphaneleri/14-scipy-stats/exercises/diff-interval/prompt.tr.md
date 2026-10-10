`diff_interval(a, b)` `b − a` ortalama farkının %95 güven aralığını Welch
testinden alsın: `stats.ttest_ind(b, a, equal_var=False).confidence_interval(0.95)`.
`[alt, üst, sıfır_içinde_mi]` döndürsün: sınırlar 2 basamak, son eleman
aralığın 0'ı içerip içermediği (`bool`).

**Beklenen çıktı:**

```
[1.42, 22.36, False]
```
