Poisson modeli güçlü bir varsayım yapar: sayımın varyansı ortalamasına
**eşit**. Gerçek veride insanlar birbirinden farklıdır (biri hiç gelmez, biri
her hafta gelir) ve varyans çoğu zaman ortalamadan büyüktür. Buna **aşırı
yayılım** (overdispersion) denir. Katsayı yine doğru yere yakın çıkar ama
standart hatalar fazla küçük kalır.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def sample(seed):
    rng = np.random.default_rng(seed)
    risk = rng.normal(0, 1, 500)
    mood = rng.gamma(1.0, 1.0, 500)          # kişiye özgü, ölçülmemiş fark
    visits = rng.poisson(np.exp(1 + 0.3 * risk) * mood)
    return pd.DataFrame({"visits": visits, "risk": risk})


df = sample(5)
print(round(df.visits.mean(), 2), round(df.visits.var(), 2))
pois = smf.glm("visits ~ risk", data=df, family=sm.families.Poisson()).fit()
print(round(pois.pearson_chi2 / pois.df_resid, 2))
families = {"poisson": sm.families.Poisson(),
            "negbin": sm.families.NegativeBinomial(alpha=1.0)}
hits = {name: 0 for name in families}
for seed in range(1000, 1200):
    data = sample(seed)
    for name, family in families.items():
        fit = smf.glm("visits ~ risk", data=data, family=family).fit()
        low, high = fit.conf_int().loc["risk"]
        hits[name] += bool(low <= 0.3 <= high)
print({k: v / 200 for k, v in hits.items()})
```

```text
2.72 10.62
3.66
{'poisson': 0.685, 'negbin': 0.945}
```

## Ne görüyoruz

- Ortalama 2,72, varyans 10,62: Poisson'un "ikisi eşit" varsayımı açıkça
  bozuk.
- Pearson ki-karenin serbestlik derecesine oranı 3,66. Poisson'a uyan veride
  bu sayı 1'e yakın olur; 1,5'in üstü aşırı yayılım işaretidir.
- 200 tekrarda Poisson'un %95 aralığı gerçek katsayıyı (0,3) yalnızca %68,5
  oranında içine aldı. Negatif binom (varyansı ortalamadan büyük olabilen
  sayım modeli) %94,5, söylediğine yakın.

## Ne zaman

- Sayım verisinde varyans ortalamadan belirgin büyükse ya da Pearson oranı
  1,5'i geçiyorsa negatif binom.
- `NegativeBinomial(alpha=...)` içindeki `alpha` yayılım miktarı;
  `smf.negativebinomial(...)` onu veriden kendisi tahmin eder.
- Yalnızca tahmin isteniyorsa Poisson yine iş görebilir; sorun belirsizlik
  hesabında.
