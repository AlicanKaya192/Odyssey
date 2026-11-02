## Formüller

| Ne | %95 güven aralığı |
|---|---|
| Ortalama | $\bar{x} \pm t_{0{,}975;\,n-1} \cdot \dfrac{s}{\sqrt{n}}$ |
| Oran (Wald) | $\hat{p} \pm 1{,}96\sqrt{\dfrac{\hat{p}(1-\hat{p})}{n}}$ |
| Oran (Wilson) | `proportion_confint(..., method="wilson")` |

## Kodda

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

x = np.array([7.2, 3.2, 10.9, 5.5, 8.1, 6.4, 12.0, 4.8])
se = stats.sem(x)
low, high = stats.t.interval(0.95, df=len(x) - 1, loc=x.mean(), scale=se)
print(round(float(low), 2), round(float(high), 2))
low, high = proportion_confint(53, 400, alpha=0.05, method="wilson")
print(round(low, 4), round(high, 4))
```

```text
4.76 9.77
0.1027 0.1692
```

## Çarpanlar

| Güven | Normal | t, 4 sd | t, 99 sd |
|---|---|---|---|
| %90 | 1,645 | 2,132 | 1,660 |
| %95 | 1,960 | 2,776 | 1,984 |
| %99 | 2,576 | 4,604 | 2,626 |

(sd: serbestlik derecesi.) Hepsi `stats.norm.ppf((1 + güven) / 2)` ve
`stats.t.ppf((1 + güven) / 2, df)` ile hesaplanır.

## Seçim

- Ortalama: her zaman t çarpanı (`stats.t.interval`).
- Oran: Wilson; Wald yalnızca büyük örneklemde ve oran 0 ya da 1'e yakın
  değilken.
- `alpha` dışarıda kalan paydır: `alpha=0.05` → %95.
