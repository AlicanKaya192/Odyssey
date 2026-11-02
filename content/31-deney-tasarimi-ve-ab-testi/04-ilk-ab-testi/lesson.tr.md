# İlk A/B Testinin Çözümlemesi

Önceki dört bölümde bir testi kurmak için gerekenleri gördük: soru ve
metrik, rastgele atama, örneklem büyüklüğü ve güven kontrolleri. Şimdi
bitmiş bir testi baştan sona çözümleyeceğiz. Sıra her zaman aynı: **önce
güven kontrolleri, sonra birincil metrik, sonra ikincil ve koruma
metrikleri, en sonda plana göre karar.**

## Plan (test başlamadan yazılmıştı)

- Değişiklik: ödeme düğmesi sayfanın üstüne taşınıyor.
- Birincil metrik: kullanıcı başına satın alma oranı (`bought`).
- İkincil metrik: kullanıcı başına gelir (`revenue`).
- Koruma metriği: alıcılar içindeki iade oranı; artmamalı.
- 50/50 atama, iki hafta, grup başına yaklaşık 15 000 kişi.
- Bu büyüklükle %80 güçle yakalanabilen en küçük etki (MDE) yaklaşık
  1,1 puan.
- Pratik eşik: düğmeyi taşımak ucuz, satın almayı **en az 0,3 puan**
  artırması yeter.
- Test: iki oran z-testi, iki yönlü, α = 0,05.

## 1. Güven kontrolü: SRM

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportions_ztest)
from ab_data import make_experiment

test = make_experiment()
n = test["group"].value_counts().sort_index()
print(n.to_dict(), round(stats.chisquare(n).pvalue, 3))
```

```text
{'A': 15041, 'B': 14959} 0.636
```

SRM p'si 0,636: grup büyüklükleri 50/50 tasarıma uyuyor. A/A
Testi ve SRM bölümündeki gibi bir kayıp işareti yok.

## 2. Güven kontrolü: denge tablosu

Testten **önceki** ziyaret sayısı ve platform değişiklikten etkilenemez;
iki grupta benzer olmalı:

```python
test["mobile"] = (test["platform"] == "mobile").astype(int)
print(test.groupby("group")[["sessions", "mobile"]].mean().round(3))
```

```text
       sessions  mobile
group                  
A         3.725   0.595
B         3.756   0.596
```

Gruplar dengeli. Artık sonuca bakabiliriz.

## 3. Birincil metrik

```python
k = test.groupby("group")["bought"].sum()
rate = k / n
p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print(rate.round(4).to_dict())
print(round(p, 4))
print(round(low, 4), round(high, 4))
```

```text
{'A': 0.1174, 'B': 0.1297}
0.0012
0.0048 0.0197
```

- Satın alma oranı A'da %11,74, B'de %12,97: 1,23
  puan fark (göreli %10,5).
- p = 0,0012: fark büyük olasılıkla şans değil.
- %95 güven aralığı 0,48 – 1,97 puan.

## 4. İkincil metrik: gelir

```python
rev_a = test.loc[test["group"] == "A", "revenue"]
rev_b = test.loc[test["group"] == "B", "revenue"]
welch = stats.ttest_ind(rev_b, rev_a, equal_var=False)
print(round(rev_a.mean(), 2), round(rev_b.mean(), 2), round(welch.pvalue, 3))
```

```text
12.55 12.75 0.737
```

Gelir B'de biraz yüksek ama p = 0,74: bu testte gelir
farkı gürültüden ayrılamıyor. Bu "gelir artmadı" demek değil; Deney Sorusu
ve Metrik Seçimi bölümünde gördüğümüz gibi gelir çok gürültülü ve bu
büyüklükteki bir test onu ölçmeye yetmez. Gelir tam bu yüzden birincil
metrik yapılmamıştı.

## 5. Koruma metriği: iade oranı

```python
buyers = test[test["bought"] == 1]
refund = buyers.groupby("group")["refunded"].agg(["sum", "count"])
print((refund["sum"] / refund["count"]).round(4).to_dict())
p_refund = proportions_ztest(refund["sum"].to_numpy(),
                             refund["count"].to_numpy())[1]
print(round(p_refund, 3))
```

```text
{'A': 0.0742, 'B': 0.0747}
0.948
```

İade oranı iki grupta neredeyse aynı (p = 0,95): koruma
metriğinde bozulma işareti yok.

## 6. Plana göre karar

Kararı veren, testten önce yazılmış kurallar:

```python
def decide(srm_p, guard_ok, low, threshold):
    if srm_p < 0.001:
        return "stop: SRM"
    if not guard_ok:
        return "stop: guardrail"
    if low >= threshold:
        return "ship"
    if low > 0:
        return "unclear"
    return "no evidence"


print(decide(stats.chisquare(n).pvalue, p_refund > 0.05, low, 0.003))
```

```text
ship
```

Aralığın alt ucu (0,48 puan) pratik eşiğin (0,3 puan) üstünde:
değişiklik uygulanır.

## Rapor

"Düğmeyi üste taşımak satın alma oranını %11,74 yerine
%12,97 yaptı: +1,23 puan (%95 güven aralığı
0,48 – 1,97, p = 0,0012). SRM ve denge kontrolleri
temiz, iade oranı değişmedi. Gelirdeki fark bu testte ölçülemedi.
Değişiklik uygulanıyor."

Raporda dört şey var: güven kontrolleri, etkinin büyüklüğü ve aralığı,
ikincil ve koruma metrikleri, plana dayanan karar.

## Özet

- Önce SRM ve denge, sonra birincil metrik.
- Birincil metrikte fark, aralık ve p birlikte okunur.
- İkincil metrikte anlamsız sonuç, gürültülü metrikte "etki yok" demek
  değildir.
- Koruma metriği bozulursa birincil metrik iyi olsa da durulur.
- Karar, testten önce yazılmış kurallarla verilir.
