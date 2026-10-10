`click_test(table)` `[[tıklayan, tıklamayan], ...]` biçiminde bir çapraz tabloyu
`stats.chi2_contingency` ile sınasın. Şunu döndürsün:

- `"stat"`: ki-kare değeri, 2 basamak
- `"dof"`: serbestlik derecesi
- `"significant"`: `p < 0.05` (`bool`)
- `"expected"`: beklenen sayılar, 1 basamaklı liste listesi

**Beklenen çıktı:**

```
26.07 1 True
[[67.5, 82.5], [67.5, 82.5]]
```
