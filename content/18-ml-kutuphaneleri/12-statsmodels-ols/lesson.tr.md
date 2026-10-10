# statsmodels: OLS

scikit-learn **tahmin** için kurulmuş: modeli eğitir, yeni satırın sonucunu
verir. Bazen soru başka: "Yaş fiyatı gerçekten etkiliyor mu, yoksa bu
katsayı şans mı? Etkinin ne kadar olduğundan ne kadar eminiz?" Bu
**çıkarım** sorusudur ve statsmodels bunun için var: her katsayının
standart hatasını, p-değerini ve güven aralığını verir. Bu bölüm en temel
modeli, sıradan en küçük kareler (OLS) regresyonunu anlatıyor.

## OLS ve katsayı tablosu

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(7)
area = rng.uniform(50, 200, 120)
age = rng.uniform(0, 40, 120)
noise = rng.normal(0, 1, 120)                 # fiyatla ilgisi yok
price = 50 + 3 * area - 2 * age + rng.normal(0, 40, 120)
X = pd.DataFrame({"area": area, "age": age, "noise": noise})
res = sm.OLS(price, sm.add_constant(X)).fit()
print(res.summary().tables[1])
print(round(res.rsquared, 3), round(res.rsquared_adj, 3))
sk = LinearRegression().fit(X, price)
print(np.round(sk.coef_, 2).tolist(), round(sk.intercept_, 2))
```

```text
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const         63.4200     11.489      5.520      0.000      40.664      86.176
area           2.9337      0.078     37.385      0.000       2.778       3.089
age           -2.5867      0.289     -8.943      0.000      -3.160      -2.014
noise         -4.1466      3.606     -1.150      0.253     -11.290       2.996
==============================================================================
0.925 0.923
[2.93, -2.59, -4.15] 63.42
```

- `sm.OLS(y, X).fit()` modeli eğitir; sonuç nesnesi (`res`) her şeyi taşır.
  `summary()` uzun bir rapor; burada yalnızca katsayı tablosunu
  (`tables[1]`) yazdırdık.
- **coef** katsayılar: scikit-learn'ün bulduklarıyla aynı (2,93, −2,59).
  Fark, yanlarındaki sütunlarda.
- **std err** (standart hata): katsayının ne kadar oynak olduğu. Başka bir
  120 evlik örnek alsak katsayı yaklaşık bu kadar değişirdi.
- **[0.025 0.975]** %95 güven aralığı: `area` için 2,78–3,09, veriyi
  üreten 3'ü içeriyor; `age` için −3,16 ile −2,01, gerçek −2'yi içeriyor.
- **P>|t|** (p-değeri): "gerçek katsayı sıfır olsaydı bu kadar büyük bir
  tahmin görme olasılığı". `noise` için 0,253: veri bu katsayının sıfırdan
  farklı olduğunu **göstermiyor**. Aralığı da sıfırı içine alıyor (−11,29 ile
  3,00). Bu "etkisi yok" demek değil, "bu veriyle ayırt edilemiyor" demek.
- R² 0,925; düzeltilmiş R² (sütun sayısını cezalandıran) 0,923.

## add_constant'ı unutmak

```python
no_const = sm.OLS(price, X).fit()
print({k: round(v, 2) for k, v in no_const.params.items()})
print(round(no_const.rsquared, 3))
```

```text
{'area': 3.28, 'age': -1.89, 'noise': -4.23}
0.989
```

- statsmodels sabit terimi kendisi **eklemez**; `sm.add_constant(X)` bir
  `const` sütunu (hep 1) ekler. Unutulunca model doğruyu sıfırdan geçmeye
  zorluyor ve bütün katsayılar kayıyor (`area` 3,28, `age` −1,89).
- Üstelik R² 0,989'a **yükseliyor**. Sabitsiz modelde R² farklı tanımlanır
  (ortalamaya göre değil, sıfıra göre); bu sayı yukarıdakiyle
  karşılaştırılamaz. Daha iyi model gibi görünen şey yanlış model.
- scikit-learn'de `LinearRegression` sabiti kendisi ekler
  (`fit_intercept=True`); statsmodels'te elle.

## Birbirine bağlı sütunlar: VIF

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

twin = area * 0.09 + rng.normal(0, 0.5, 120)   # alanın neredeyse kopyası
X2 = sm.add_constant(pd.DataFrame({"area": area, "twin": twin, "age": age}))
res2 = sm.OLS(price, X2).fit()
print({k: round(v, 2) for k, v in res2.params.items()})
print({k: round(v, 2) for k, v in res2.bse.items()})
vif = [variance_inflation_factor(X2.values, i) for i in range(1, 4)]
print([round(float(v), 1) for v in vif])
```

```text
{'const': 62.7, 'area': 3.33, 'twin': -4.34, 'age': -2.58}
{'const': 11.62, 'area': 0.7, 'twin': 7.54, 'age': 0.29}
[79.1, 78.9, 1.0]
```

- `twin` alanın gürültülü bir kopyası (korelasyon 0,99'un üstünde). İkisi
  aynı bilgiyi taşıyınca model etkiyi aralarında keyfi paylaştırıyor:
  `area` 3,33, `twin` −4,34 (eksi!). Fiyat yine iyi tahmin ediliyor ama
  katsayılar yorumlanamaz.
- `area`'nın standart hatası 0,08'den 0,7'ye, yaklaşık 9 katına çıktı.
- **VIF** (varyans şişirme çarpanı) bunu sayıyla söyler: `area` ve `twin`
  79, `age` 1. Kabaca 10'un üstü "bu sütun başkalarıyla neredeyse aynı".
  Çare: birini çıkarmak ya da ikisini tek bir sütunda birleştirmek.

## Tahmin ve iki aralık

```python
new = pd.DataFrame({"area": [100, 180], "age": [10, 30], "noise": [0, 0]})
pred = res.get_prediction(sm.add_constant(new, has_constant="add"))
print(pred.summary_frame(alpha=0.05).round(1))
```

```text
    mean  mean_se  mean_ci_lower  mean_ci_upper  obs_ci_lower  obs_ci_upper
0  330.9      4.9          321.3          340.6         256.9         405.0
1  513.9      5.9          502.2          525.6         439.5         588.2
```

- `mean` tahmin. Yanında **iki** aralık var:
- `mean_ci` (321,3–340,6): bu özellikteki evlerin **ortalama** fiyatı için
  aralık. Dar, çünkü ortalama iyi kestiriliyor.
- `obs_ci` (256,9–405,0): **tek bir** evin fiyatı için aralık. Çok daha
  geniş, çünkü tek bir evin kendi gürültüsü de içinde.
- "Bu ev ne kadara satılır?" sorusunun cevabı `obs_ci`'dir. `mean_ci`'yi
  tek ev için vermek fazla emin konuşmaktır.
- `has_constant="add"`: yeni veride de `const` sütunu gerekir. Varsayılan
  `add_constant` zaten sabit bir sütun görürse eklemez; **tek satırlık**
  veride her sütun sabit göründüğü için `const` eklenmez ve tahmin hata
  verir. `"add"` her zaman ekler.

## Özet

- Tahmin için scikit-learn, "etki ne kadar ve ne kadar eminiz" için
  statsmodels.
- `sm.add_constant` unutulmaz; unutulursa R² yanıltıcı yükselir.
- Katsayı tablosu: katsayı, standart hata, p-değeri, güven aralığı.
- Büyük p-değeri "etkisi yok" değil, "ayırt edilemiyor" demektir.
- Birbirine bağlı sütunlar katsayıları bozar; VIF ile bakılır.
- Tek bir gözlem için `obs_ci`, ortalama için `mean_ci`.
