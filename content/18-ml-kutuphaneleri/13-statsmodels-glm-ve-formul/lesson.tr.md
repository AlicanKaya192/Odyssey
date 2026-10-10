# statsmodels: GLM ve Formüller

Önceki bölümde `sm.OLS(y, X)` ile modeli dizilerle kurduk: sabit sütunu
elle ekledik, metin sütunu olsaydı onu da kendimiz sayıya çevirecektik.
statsmodels'in ikinci arayüzü **formül**: modeli R dilindeki gibi bir
cümleyle yazarsın (`"price ~ area + C(city)"`), gerisini kütüphane yapar.
Bu bölüm formül dilini, kategorik sütunları, etkileşimi ve doğrusal
regresyonun genelleştirilmiş hâllerini (GLM) anlatıyor: evet/hayır sonucu
için lojistik, sayım sonucu için Poisson.

## Formülle OLS

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(11)
df = pd.DataFrame({
    "area": rng.uniform(50, 200, 300).round(),
    "city": rng.choice(["Ankara", "Izmir", "Istanbul"], 300),
    "age": rng.uniform(0, 40, 300).round(),
})
bonus = df["city"].map({"Ankara": 0, "Izmir": 40, "Istanbul": 120})
noise = rng.normal(0, 30, 300)
df["price"] = 50 + 3 * df["area"] - 2 * df["age"] + bonus + noise
res = smf.ols("price ~ area + age + C(city)", data=df).fit()
for name, value in res.params.items():
    print(f"{name:20} {value:8.2f}")
```

```text
Intercept               40.57
C(city)[T.Istanbul]    118.14
C(city)[T.Izmir]        43.82
area                     3.04
age                     -1.88
```

- `smf.ols(formül, data=df)`: `~` işaretinin solu hedef, sağı açıklayıcılar.
  Sütunlar DataFrame'den adlarıyla alınır, **sabit terim kendiliğinden
  eklenir** (`Intercept`).
- `C(city)` "bu sütun kategorik" demek. Formül onu kukla (dummy) sütunlara
  çevirir: `C(city)[T.Istanbul]`, `C(city)[T.Izmir]`. Ankara **taban**
  (abece sırasında ilk): diğer şehirlerin katsayısı Ankara'ya göre fark.
- Veriyi üreten farklar Izmir 40, Istanbul 120; model 43,82 ve 118,14 buldu.

## Tabanı değiştirmek ve tahmin

```python
formula = "price ~ area + age + C(city, Treatment('Istanbul'))"
other = smf.ols(formula, data=df).fit()
print(other.params.filter(like="T.").round(2).tolist())
new = pd.DataFrame({"area": [100], "age": [10], "city": ["Izmir"]})
print(res.predict(new).round(1).tolist())
```

```text
[-118.14, -74.32]
[370.1]
```

- `Treatment('Istanbul')` tabanı İstanbul yapar: artık Ankara −118,14,
  Izmir −74,32 (İstanbul'a göre; `filter(like="T.")` yalnızca şehir
  satırlarını seçti). Model aynı, yalnızca okuma biçimi
  değişti; `area` ve `age` katsayıları aynı kaldı.
- Tahmin için yeni veri **ham** verilir: şehir adı metin olarak. Formül,
  eğitimde öğrendiği kodlamayı yeni satıra kendisi uygular; `add_constant`
  ya da kukla sütun yazmak gerekmez.

## Etkileşim ve dönüşümler

```python
extra = 1.5 * df["area"] * (df["city"] == "Istanbul")  # İstanbul farkı
df["price2"] = 50 + 3 * df["area"] + extra - 2 * df["age"] + rng.normal(0, 30, 300)
inter = smf.ols("price2 ~ area * C(city) + age", data=df).fit()
print({k: round(v, 2) for k, v in inter.params.items() if "area" in k})
curve = smf.ols("price ~ area + I(area ** 2) + np.log(age + 1)", data=df).fit()
print(curve.model.exog_names)
```

```text
{'area': 3.04, 'area:C(city)[T.Istanbul]': 1.49, 'area:C(city)[T.Izmir]': -0.02}
['Intercept', 'area', 'I(area ** 2)', 'np.log(age + 1)']
```

- Bu sefer İstanbul'da metrekare **daha pahalı**: alan başına 3 yerine
  4,5. `area * C(city)` hem ayrı etkileri hem de **etkileşimi**
  (`area:C(city)[T.Istanbul]`) ekler: "alanın etkisi şehre göre değişiyor
  mu?" Model farkı 1,49 buldu (gerçek 1,5); Izmir için −0,02, yani fark yok.
- `I(...)` içindeki işlem olduğu gibi hesaplanır: `I(area ** 2)` kare
  sütunu. (`I` olmadan `**` formülde başka anlama gelir.) `np.log(...)` gibi
  NumPy fonksiyonları da doğrudan yazılır.

## Lojistik regresyon: smf.logit

```python
from sklearn.linear_model import LogisticRegression

score = rng.normal(0, 1, 1000)
premium = rng.integers(0, 2, 1000)
chance = 1 / (1 + np.exp(-(-1 + 0.8 * score + 1.2 * premium)))
d2 = pd.DataFrame({"y": (rng.random(1000) < chance).astype(int),
                   "score": score, "premium": premium})
logit = smf.logit("y ~ score + premium", data=d2).fit(disp=0)
print({k: round(v, 3) for k, v in logit.params.items()})
print({k: round(v, 2) for k, v in np.exp(logit.params).items()})
sk = LogisticRegression().fit(d2[["score", "premium"]], d2["y"])
print(sk.coef_.round(3).tolist())
```

```text
{'Intercept': -1.03, 'score': 0.746, 'premium': 1.22}
{'Intercept': 0.36, 'score': 2.11, 'premium': 3.39}
[[0.739, 1.194]]
```

- `smf.logit` sonucu 0/1 olan model; `disp=0` eğitim mesajlarını susturur.
  Katsayılar veriyi üretenlere yakın (0,746 ve 1,22; gerçek 0,8 ve 1,2).
- Lojistik katsayı log-olasılık oranı; `np.exp` ile **olasılık oranına**
  (odds ratio) çevrilir: premium üyelikte olayın olasılık oranı 3,39 kat.
  `score` bir birim artınca 2,11 kat.
- scikit-learn'ün `LogisticRegression`'ı aynı veride biraz farklı (0,739,
  1,194): varsayılan olarak **cezalı** (`C=1`), katsayıları sıfıra doğru
  çeker. Yorum için katsayı isteniyorsa statsmodels (ya da `C=np.inf`).

## Sayım sonucu: Poisson GLM

Bir sigorta şirketi müşteri başına hasar sayısını inceliyor. Müşteriler
farklı sürelerle (10–365 gün) sigortalı; uzun süre sigortalı olan doğal
olarak daha çok hasar bildirir.

```python
days = rng.integers(10, 365, 500)
risk = rng.normal(0, 1, 500)
claims = rng.poisson(np.exp(-4 + 0.5 * risk) * days)
d3 = pd.DataFrame({"claims": claims, "risk": risk, "days": days})
poisson = sm.families.Poisson()
fair = smf.glm("claims ~ risk", data=d3, family=poisson,
               offset=np.log(d3["days"])).fit()
naive = smf.glm("claims ~ risk", data=d3, family=poisson).fit()
print({k: round(v, 3) for k, v in fair.params.items()})
print({k: round(v, 3) for k, v in naive.params.items()})
print(round(np.exp(fair.params["risk"]), 3))
line = smf.ols("claims ~ risk", data=d3).fit()
print(int((line.fittedvalues < 0).sum()))
```

```text
{'Intercept': -4.009, 'risk': 0.496}
{'Intercept': 1.283, 'risk': 0.44}
1.642
4
```

- `smf.glm(..., family=Poisson())`: sonuç sayım (0, 1, 2, ...), model
  sayının **ortalamasının logaritmasını** doğrusal kurar. Bu yüzden tahmin
  hiç eksi olmaz.
- `offset=np.log(days)` "her müşteri farklı süre gözlendi" der; model
  günlük **oranı** öğrenir. Katsayılar veriyi üretenlerle aynı: −4,009 ve
  0,496 (gerçek −4 ve 0,5).
- Offset unutulunca sabit tamamen yanlış (1,283) ve risk katsayısı 0,44:
  süre bilgisi başka yere sızıyor.
- `np.exp(0.496)` = 1,642: risk bir birim artınca hasar **oranı** %64
  artıyor (oran oranı, rate ratio).
- Aynı veriye düz doğrusal regresyon 4 müşteri için **eksi** hasar sayısı
  tahmin ediyor.

## Özet

- Formül: `smf.ols("y ~ a + b + C(c)", data=df)`; sabit kendiliğinden,
  kategorik `C()`, taban `Treatment('...')`.
- Etkileşim `a * C(c)` (`a:C(c)` yalnızca etkileşim), dönüşüm `I(a ** 2)`,
  `np.log(a)`.
- Evet/hayır sonucu: `smf.logit`; `np.exp(params)` olasılık oranı.
- Sayım sonucu: `smf.glm(..., family=sm.families.Poisson())`; farklı
  gözlem süresi varsa `offset=np.log(süre)`.
