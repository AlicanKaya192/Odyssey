## Formüller

| Ne | Formül |
|---|---|
| Oran | $\hat{p} = k / n$ |
| Ortak oran ($H_0$ altında) | $\hat{p} = (k_A + k_B) / (n_A + n_B)$ |
| Farkın standart hatası | $\sqrt{\hat{p}(1-\hat{p})(1/n_A + 1/n_B)}$ |
| Test istatistiği | $z = (\hat{p}_B - \hat{p}_A) / SE$ |
| Göreli artış | $(\hat{p}_B - \hat{p}_A) / \hat{p}_A$ |

## Kodda

```python
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.proportion import confint_proportions_2indep

k_b, n_b, k_a, n_a = 130, 1000, 105, 1000
z, p = proportions_ztest([k_b, k_a], [n_b, n_a])
low, high = confint_proportions_2indep(k_b, n_b, k_a, n_a, method="newcomb")
fisher = stats.fisher_exact([[k_b, n_b - k_b], [k_a, n_a - k_a]])
print(round(z, 3), round(p, 4), round(fisher.pvalue, 4))
print(round(low, 4), round(high, 4))
```

```text
1.736 0.0826 0.0954
-0.0033 0.0533
```

- `proportions_ztest(sayılar, örneklemler)`: sıra "ilk eksi ikinci".
- `confint_proportions_2indep(k1, n1, k2, n2)`: `k1/n1 − k2/n2` farkının aralığı.
- `fisher_exact` 2×2 tablo ister: her satır bir grup, sütunlar
  `[evet, hayır]`.
- Binlerce kullanıcılı testte z ve Fisher p'leri birbirine yakın çıkar.

## Hangi test?

| Durum | Test |
|---|---|
| Büyük gruplar | z-testi |
| Herhangi bir hücrede beklenen sayı < 5 | Fisher |
| İkiden çok grup | ki-kare (bir sonraki bölüm) |
