`ab_report(a, b)` iki grubu Welch testiyle karşılaştırıp kısa bir rapor
döndürsün:

- `"diff"`: `b` ortalaması − `a` ortalaması, 2 basamak
- `"interval"`: farkın %95 güven aralığı `[alt, üst]`, 2 basamak
- `"decision"`: aralık sıfırı içeriyorsa `"unclear"`, tamamı sıfırın üstündeyse
  `"b better"`, altındaysa `"a better"`

Test: `stats.ttest_ind(b, a, equal_var=False)` ve `.confidence_interval()`.

**Beklenen çıktı:**

```
11.89 [1.42, 22.36]
b better
```
