OLS'nin standart hataları bir varsayıma dayanır: hatanın büyüklüğü her
satırda aynı. Ev fiyatında bu çoğu zaman tutmaz: 50 m²'lik evin fiyatı
birkaç bin, 400 m²'lik evinki yüz binlerce lira sapabilir. Varsayım
bozulunca katsayı yine doğru çıkar ama **güven aralığı yalan söyler**.

```python
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan


def sample(seed):
    rng = np.random.default_rng(seed)
    area = rng.lognormal(4.3, 0.5, 200)                  # çoğu küçük ev
    noise = rng.normal(0, 1, 200) * area ** 1.5 * 0.05   # büyük evde büyük hata
    return sm.add_constant(area), 50 + 3 * area + noise


X, y = sample(3)
plain = sm.OLS(y, X).fit()
robust = sm.OLS(y, X).fit(cov_type="HC3")
print(round(het_breuschpagan(plain.resid, X)[1], 4))
print(round(plain.bse[1], 3), round(robust.bse[1], 3))
hits = {"plain": 0, "HC3": 0}
for seed in range(100, 600):
    X, y = sample(seed)
    for name, kind in [("plain", "nonrobust"), ("HC3", "HC3")]:
        low, high = sm.OLS(y, X).fit(cov_type=kind).conf_int()[1]
        hits[name] += bool(low <= 3 <= high)
print({k: v / 500 for k, v in hits.items()})
```

```text
0.0
0.085 0.309
{'plain': 0.578, 'HC3': 0.934}
```

## Ne görüyoruz

- Breusch–Pagan testinin p-değeri 0: hata varyansı sabit değil.
- Alanın katsayısının standart hatası klasik hesapla 0,085, dayanıklı
  (`HC3`) hesapla 0,309: gerçek belirsizlik dört kata yakın büyük.
- Aynı deneyi 500 kez tekrarladık ve %95 güven aralığının gerçek katsayıyı
  (3) kaç kez içine aldığını saydık. Klasik aralık yalnızca %57,8'inde
  yakaladı; "%95 eminim" derken yarı yarıya yanılıyor. HC3 aralığı %93,4,
  söylediğine yakın.

## Ne zaman

- Artıklar uydurulan değerle birlikte büyüyorsa (huni biçimi) ya da
  Breusch–Pagan küçük p veriyorsa `cov_type="HC3"`.
- Katsayılar değişmez; yalnızca standart hata, p-değeri ve aralık değişir.
- Varyans sabitse HC3 de klasik hesaba yakın çıkar; şüphede kullanmanın
  bedeli küçük.
