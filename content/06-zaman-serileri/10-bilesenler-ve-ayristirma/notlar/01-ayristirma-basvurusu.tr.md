## Üç araç

| | `seasonal_decompose` | `STL` | `MSTL` |
|---|---|---|---|
| Yöntem | Hareketli ortalama | LOESS (yerel düzleştirme) | Art arda STL |
| Model | Toplamsal ya da çarpımsal | Yalnızca toplamsal | Yalnızca toplamsal |
| Uçlarda trend | `NaN` (yarım periyot) | Tanımlı | Tanımlı |
| Mevsim | Sabit | Zamanla değişebilir | Zamanla değişebilir |
| Aykırı değer | Dayanıksız | `robust=True` | `stl_kwargs={"robust": True}` |
| Periyot sayısı | Bir | Bir | Birden çok |
| Hız | Çok hızlı | Hızlı | Yavaşça |

Hepsi `statsmodels.tsa.seasonal` içinde.

## Çağrılar

```python
from statsmodels.tsa.seasonal import MSTL, STL, seasonal_decompose

r = seasonal_decompose(s, model="additive", period=7)
r = seasonal_decompose(p, model="multiplicative", period=12)

r = STL(s, period=7, robust=True).fit()
r = MSTL(s, periods=(7, 365)).fit()

r.observed, r.trend, r.seasonal, r.resid
fig = r.plot()
```

`MSTL`'de `r.seasonal` bir tablo: periyot başına bir sütun (`seasonal_7`,
`seasonal_365`).

İndeksin sıklığı belliyse (`asfreq("D")`, `asfreq("MS")`) statsmodels periyodu
kendisi tahmin edebiliyor, ama her zaman istediğini seçmiyor. **`period`'u
kendin yaz.**

## Periyot seçimi

| Veri sıklığı | Desen | `period` |
|---|---|---|
| Saatlik | Günlük | 24 |
| Saatlik | Haftalık | 168 |
| Günlük | Haftalık | 7 |
| Günlük | Yıllık | 365 |
| Haftalık | Yıllık | 52 |
| Aylık | Yıllık | 12 |
| Çeyreklik | Yıllık | 4 |

Veride periyottan en az **iki tam tur** olmalı; güvenilir bir desen için üç ve
üstü.

## Çift periyotta trend: 2×12 ortalama

Periyot tek sayıysa (7) ortalanmış pencerenin bir orta noktası var. Çift
sayıda (12) yok: pencere ya 6 ay geriye 5 ay ileriye bakar ya da tersine. Klasik
çözüm 12'lik ortalamanın üstüne 2'lik bir ortalama daha almak:

```python
trend = p.rolling(12).mean().rolling(2).mean().shift(-6)
```

Sonuç 13 aya yayılan, iki uçtaki ayın yarım ağırlık aldığı simetrik bir
ortalama. `seasonal_decompose` çift periyotta tam olarak bunu yapıyor
(ölçüldü); `p.rolling(12, center=True).mean()` ise aynı sonucu **vermiyor**.

## Toplamsal mı, çarpımsal mı: karar

1. Seriyi çiz. Dalgaların boyu düzey yükseldikçe büyüyor mu?
2. Yıl bazında `max - min` ve `max / min` hesapla. Hangisi sabit?
   Fark sabitse toplamsal, oran sabitse çarpımsal.
3. İkisini de dene, kalıntıyı yıla göre grupla. Kalıntının boyu yıldan yıla
   değişiyorsa o model yanlış.

Seride sıfır ya da eksi değer varsa çarpımsal model kullanılamaz. Emin
değilsen: logaritma al, toplamsal ayrıştır.

## Çarpımsal modelde birimler

| Bileşen | Toplamsal | Çarpımsal |
|---|---|---|
| Trend | Serinin birimi | Serinin birimi |
| Mevsim | Serinin birimi, toplamı 0 | Oran, ortalaması 1 |
| Kalıntı | Serinin birimi, 0 çevresinde | Oran, 1 çevresinde |

Çarpımsal kalıntı 1.03 ise gözlem beklenenin %3 üstünde.

## STL'in ayarları

```python
STL(s, period=7, seasonal=7, trend=None, robust=False)
```

- `seasonal`: mevsimin ne kadar hızlı değişebileceği (tek sayı, en az 7).
  Küçük değer: mevsim yıldan yıla serbestçe değişir. Büyük değer: neredeyse
  sabit mevsim, klasik yönteme yaklaşır.
- `trend`: trend düzleştiricisinin boyu (tek sayı). Büyüdükçe trend düzleşir.
  Boş bırakılırsa periyottan hesaplanır.
- `robust`: aykırı günlerin ağırlığını düşürür. Aykırı değer varsa aç;
  `fit.weights` hangi günlerin kısıldığını gösterir.

## Bileşenlerin gücü

Mevsim ne kadar belirgin? 0 ile 1 arasında bir ölçü:

$$F_S = \max\left(0,\; 1 - \frac{\operatorname{Var}(\text{kalıntı})}{\operatorname{Var}(\text{mevsim} + \text{kalıntı})}\right)$$

Trend için aynı formül, mevsim yerine trend yazılarak.

```python
strength = 1 - r.resid.var() / (r.seasonal + r.resid).var()
```

Günlük satışta haftalık mevsimin gücü 0.92, trendin gücü 0.91: ikisi de çok
belirgin. 0.3'ün altı zayıf, ayırmaya değmeyebilir. Çok sayıda seriyi
(yüzlerce ürün) sınıflandırırken kullanışlı: hangisi mevsimsel, hangisi değil.

## Arındırma

```python
adjusted = s - r.seasonal        # toplamsal
adjusted = p / r.seasonal        # carpimsal
detrended = s - r.trend          # trendsiz: yalnizca desen ve gurultu
```
