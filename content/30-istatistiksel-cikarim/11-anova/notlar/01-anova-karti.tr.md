## Formüller

| Ne | Formül |
|---|---|
| Gruplar arası kareler toplamı | $\sum_g n_g (\bar{x}_g - \bar{x})^2$ |
| Grup içi kareler toplamı | $\sum_g \sum_i (x_{gi} - \bar{x}_g)^2$ |
| F | $\dfrac{SS_{arası} / (k-1)}{SS_{içi} / (N-k)}$ |
| Etki büyüklüğü | $\eta^2 = SS_{arası} / (SS_{arası} + SS_{içi})$ |

## Kodda

```python
from scipy import stats
from statsmodels.stats.oneway import anova_oneway
from ab_data import make_layout_test

test = make_layout_test()
groups = [g["minutes"] for _, g in test.groupby("layout")]
classic = stats.f_oneway(*groups)
welch = anova_oneway(test["minutes"], test["layout"], use_var="unequal")
print(round(classic.statistic, 3), f"{classic.pvalue:.1e}")
print(round(welch.statistic, 3), f"{welch.pvalue:.1e}")
```

```text
7.692 4.8e-05
7.314 9.2e-05
```

- `stats.f_oneway`: klasik ANOVA, eşit varyans varsayar.
- `anova_oneway(..., use_var="unequal")`: Welch ANOVA; sapmalar farklıysa.
  Burada sapmalar birbirine yakın, iki sonuç da benzer.
- `stats.tukey_hsd(*groups)`: hangi çiftlerin farklı olduğu; `.statistic`
  ortalama farkları, `.pvalue` düzeltilmiş p'ler.

## Akış

1. Grupların ortalama ve sapmalarına bak.
2. ANOVA (sapmalar çok farklıysa Welch).
3. p küçükse Tukey HSD ile çiftlere bak.
4. Raporla: grup ortalamaları, F, p, $\eta^2$ ve farklı çıkan çiftler.

## Kaç çift?

$k$ grup için $k(k-1)/2$ çift: 4 grupta 6, 6 grupta 15, 10 grupta 45.
