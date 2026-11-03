## CUPED üç satırda

```python
import numpy as np
import statsmodels.formula.api as smf
from ab_data import make_engagement_test

test = make_engagement_test()
y = test["minutes"].to_numpy()
x = test["pre_minutes"].to_numpy()
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
test["adjusted"] = y - theta * (x - x.mean())
test["b"] = (test["group"] == "B").astype(int)
diff = test.groupby("b")["adjusted"].mean().diff().iloc[-1]
model = smf.ols("minutes ~ b + pre_minutes", data=test).fit()
print(round(diff, 3), round(model.params["b"], 3))
```

```text
1.04 1.04
```

İkinci sayı aynı soruyu regresyonla soruyor: `pre_minutes` ortak değişken
olarak modelde. CUPED, bu regresyonun elle yapılan hâlidir; sonuçlar
neredeyse aynı çıkar.

## Kazanç ne kadar?

Kalan varyans yaklaşık 1 − ρ²:

| ρ (önce ile sonra) | kalan varyans |
|---|---|
| 0,3 | 0,91 |
| 0,5 | 0,75 |
| 0,7 | 0,51 |
| 0,9 | 0,19 |

ρ 0,3 civarındaysa kazanç küçüktür; aynı metriğin önceki değeri genellikle
en yüksek korelasyonu verir.

## Kontrol listesi

- X atamadan **önce** ölçüldü mü?
- X iki grupta dengeli mi? (A/A Testi ve Örneklem Oranı Uyumsuzluğu
  bölümündeki denge denetimi)
- Önceki verisi olmayan yeni kullanıcılar için X ne olacak? (aşağıdaki
  not)
- θ iki grubun birleşik verisinden hesaplandı mı?
