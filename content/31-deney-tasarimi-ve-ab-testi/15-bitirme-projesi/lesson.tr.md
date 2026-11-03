# Bitirme Projesi

Bu bölümde bir deneyi baştan sona, modüldeki her adımı kullanarak
çözümlüyoruz. Bir e-ticaret sitesi ücretsiz kargo sınırını düşürmeyi
düşünüyor. Soru: **bu değişiklik satın almayı artırıyor mu ve bunu yaparken
bir şeyi bozuyor mu?** Veriyi biz ürettik; gerçek etkiyi sona kadar
söylemeyelim, çözümleme kendisi bulsun.

## 1. Plan (testten önce)

Deney Sorusu ve Metrik Seçimi bölümündeki gibi plan yazılmış:

- **Birincil metrik:** satın alma oranı (kullanıcı başına, 0/1).
- **Pratik eşik:** en az 0,3 puan artış.
- **İkincil metrik:** kullanıcı başına gelir (CUPED ile, ortak değişken
  testten önceki dört haftanın harcaması).
- **Koruma metriği:** alıcılarda iade oranı; 2 puandan fazla artış kabul
  edilmez.
- **Segment:** yalnızca platform (önceden yazılmış tek segment).
- **Örneklem:** taban oran %10, en küçük önemli fark 1 puan.

```python
import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportion_effectsize,
                                          proportions_ztest)
from ab_data import make_capstone

h = proportion_effectsize(0.11, 0.10)
need = NormalIndPower().solve_power(h, alpha=0.05, power=0.8)
print(int(np.ceil(need)))
```

```text
14745
```

Grup başına 14 745 kullanıcı gerekiyor (Örneklem Büyüklüğü
bölümü). Test iki hafta sürdü ve 40 000 kullanıcı topladı.

## 2. Güven denetimleri

```python
test = make_capstone()
n = test.groupby("group").size()
print(n.to_dict(), round(stats.chisquare(n).pvalue, 3))
print(test.groupby("group")["pre_spend"].mean().round(2).to_dict())
```

```text
{'A': 19902, 'B': 20098} 0.327
{'A': 132.21, 'B': 131.59}
```

SRM p'si 0,327: 0,001 eşiğinin çok üstünde, atama sağlam (A/A
Testi ve Örneklem Oranı Uyumsuzluğu bölümü). Testten önceki harcama iki
grupta neredeyse aynı: gruplar dengeli. Her grupta yaklaşık 20 000 kişi
var, plandaki 14 745 kişiden fazla.

## 3. Birincil metrik

```python
k = test.groupby("group")["bought"].sum()
p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print((k / n).round(4).to_dict(), f"{p:.1e}")
print(round(low * 100, 2), round(high * 100, 2))
```

```text
{'A': 0.1007, 'B': 0.1154} 2.4e-06
0.86 2.07
```

Satın alma %10,07 yerine %11,54. Farkın %95 aralığı
0,86 ile 2,07 puan: tamamen 0,3 puanlık eşiğin üstünde.

## 4. İkincil metrik: gelir, CUPED ile

```python
y = test["revenue"].to_numpy()
x = test["pre_spend"].to_numpy()
is_b = (test["group"] == "B").to_numpy()
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
adjusted = y - theta * (x - x.mean())
for values in (y, adjusted):
    welch = stats.ttest_ind(values[is_b], values[~is_b], equal_var=False)
    diff = values[is_b].mean() - values[~is_b].mean()
    print(round(diff, 2), round(welch.pvalue, 4))
print(round(np.corrcoef(x, y)[0, 1], 2), round(adjusted.var() / y.var(), 3))
```

```text
1.01 0.0014
1.03 0.0009
0.21 0.957
```

Kullanıcı başına gelir B'de yaklaşık 1,01 TL fazla. Testten
önceki harcama ile gelirin korelasyonu yalnızca 0,21, bu yüzden
CUPED varyansın ancak %4,3 kadarını siliyor (Varyans Azaltma:
CUPED bölümündeki 1 − ρ²). Kazanç küçük ama bedava; gelir yine de bir
ikincil metrik olarak kalıyor.

## 5. Koruma metriği: iade

```python
buyers = test[test["bought"] == 1]
refunds = buyers.groupby("group")["refunded"].agg(["sum", "count"])
print((refunds["sum"] / refunds["count"]).round(4).to_dict())
low_r, high_r = confint_proportions_2indep(
    refunds.loc["B", "sum"], refunds.loc["B", "count"],
    refunds.loc["A", "sum"], refunds.loc["A", "count"])
print(round(low_r * 100, 2), round(high_r * 100, 2))
```

```text
{'A': 0.0773, 'B': 0.0716}
-2.16 0.99
```

İade oranı farkının aralığının üst ucu 0,99 puan: plandaki 2
puanlık sınırın altında. Koruma metriği bozulmadı.

## 6. Önceden yazılmış segment: platform

```python
for name, part in test.groupby("platform"):
    rates = part.groupby("group")["bought"].mean()
    print(name, round(rates["B"] / rates["A"] - 1, 3), len(part))
```

```text
desktop 0.169 17991
mobile 0.122 22009
```

İki platformda da B önde. Segmentler ve Simpson Paradoksu bölümünde
gördüğümüz gibi bu sayılar gürültülü; aralarındaki farkı yorumlamıyoruz,
yalnızca "iki platformda da aynı yönde" diyoruz.

## 7. Karar ve rapor

```python
def verdict(low, high, threshold=0.003):
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


srm_ok = stats.chisquare(n).pvalue > 0.001
guard_ok = high_r < 0.02
print(srm_ok, guard_ok, verdict(low, high))
```

```text
True True ship
```

Rapor:

> Ücretsiz kargo sınırını düşürmek satın almayı %10,07 yerine
> %11,54 yaptı (%95 aralık 0,86 – 2,07 puan,
> önceden yazılmış 0,3 puanlık eşiğin üstünde). SRM ve denge temiz, iade
> oranı plandaki sınırın içinde, iki platformda da aynı yönde. Gelir artışı
> ikincil metrik olarak not edildi. Karar: uygulanıyor. Sınırlar: iki
> haftalık test; yenilik etkisi için uygulamadan sonra küçük bir tutma
> grubu bırakılacak.

Veriyi ürettiğimiz için gerçeği de söyleyebiliriz: B satın almayı gerçekte
%12 artırıyordu; sipariş tutarı ve iade değişmiyordu. Çözümleme bunu doğru
buldu.

## Özet

- Plan testten önce: metrikler, eşikler, örneklem, segment.
- Önce güven (SRM, denge), sonra birincil metrik, sonra ikincil ve koruma.
- CUPED'in kazancı korelasyona bağlıdır; burada küçük.
- Karar önceden yazılmış kurallarla verilir ve rapor sınırlarıyla birlikte
  yazılır.
