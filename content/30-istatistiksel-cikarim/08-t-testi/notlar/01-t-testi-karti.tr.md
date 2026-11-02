## Hangi t-testi?

| Veri | Test | Kod |
|---|---|---|
| Tek grup, bilinen bir değere karşı | tek örneklem | `stats.ttest_1samp(x, mu0)` |
| İki ayrı grup | Welch | `stats.ttest_ind(b, a, equal_var=False)` |
| Aynı birimler, iki ölçüm | eşli | `stats.ttest_rel(before, after)` |

## Sonuç nesnesi

```python
from scipy import stats

a = [8.1, 6.5, 9.9, 7.2, 5.8, 8.8, 7.7, 6.9]
b = [9.4, 8.2, 11.0, 7.9, 9.1, 10.3, 8.6, 9.8]
result = stats.ttest_ind(b, a, equal_var=False)
low, high = result.confidence_interval(0.95)
print(round(result.statistic, 3), round(result.pvalue, 4))
print(round(result.df, 1))
print(round(low, 2), round(high, 2))
```

```text
2.807 0.0145
13.4
0.39 2.96
```

- `statistic`: t; `pvalue`: p; `df`: serbestlik derecesi (Welch'te kesirli
  çıkabilir).
- `confidence_interval(0.95)`: ilk grup eksi ikinci grup farkının aralığı.
  Sıra önemli: `ttest_ind(b, a)` "b − a" demek.

## Formüller

- Welch: $t = \dfrac{\bar{x}_B - \bar{x}_A}{\sqrt{s_A^2/n_A + s_B^2/n_B}}$
- Eşli: farklar $d_i$ üzerinden $t = \dfrac{\bar{d}}{s_d/\sqrt{n}}$

## Seçerken üç soru

1. Gruplar aynı birimlerden mi oluşuyor? Evet → eşli.
2. Sapmalar ve grup boyları farklı olabilir mi? Hep "olabilir" say → Welch.
3. Örneklem küçük ve veri çok çarpık mı? Evet → parametrik olmayan test ya
   da bootstrap.
