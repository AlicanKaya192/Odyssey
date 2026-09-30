## Kurulum

```python
from statsmodels.tsa.arima.model import ARIMA

fit = ARIMA(
    train,
    order=(p, d, q),
    seasonal_order=(P, D, Q, m),     # mevsim yoksa yazilmaz
).fit()
```

`train` düzenli aralıklı bir tarih indeksi taşımalı (`asfreq`); o zaman
`forecast` tarihleri kendisi üretir.

## Sonuç nesnesi

| Özellik | İçerik |
|---|---|
| `fit.params` | Katsayılar: `const`, `ar.L1`, `ma.L1`, `ar.S.L12`, `ma.S.L12`, `sigma2` |
| `fit.pvalues` | Her katsayının p-değeri |
| `fit.summary()` | Bütün tablo; yalnızca katsayılar için `.tables[1]` |
| `fit.aic`, `fit.bic` | Bilgi ölçütleri; küçük olan iyi |
| `fit.resid` | Eğitimdeki bir adımlık kalıntılar |
| `fit.fittedvalues` | Eğitimdeki bir adımlık tahminler |
| `fit.forecast(h)` | Sonraki `h` adım |
| `fit.get_forecast(h)` | Tahmin + aralık: `.predicted_mean`, `.conf_int()` (Bölüm 20) |

## Tanıdık yüzler

Şimdiye kadar gördüğün yöntemlerin çoğu ARIMA ailesinin özel hâlleri:

| ARIMA | Aynı şey |
|---|---|
| (0,0,0) | Beyaz gürültü; tahmin ortalama |
| (0,1,0) | Rastgele yürüyüş; tahmin naif |
| (0,1,0) + sabit | Kayma (drift) |
| (0,1,1) | Basit üstel düzleştirme |
| (0,2,2) | Holt (toplamsal trend) |
| (0,0,0)(0,1,0)ₘ | Mevsimsel naif |
| (0,1,1)(0,1,1)ₘ | Toplamsal Holt–Winters'a çok yakın |
| (1,0,0) | AR(1): ortalamaya dönen seri |

Basit üstel düzleştirmede `α = 1 + θ`: MA katsayısı −0.8 ise `α = 0.2`.

## Katsayıları okumak

| Katsayı | Anlamı |
|---|---|
| `ar.L1 = 0.7` | Bugünkü sapmanın %70'i yarına kalıyor |
| `ar.L1` ≈ 1 | Neredeyse rastgele yürüyüş; `d`'yi bir artır |
| `ar.L1 < 0` | Seri bir yukarı bir aşağı gidiyor |
| `ma.L1 = −0.8`, `d = 1` | Sürprizin %20'si kalıcı; düzey yavaş uyuyor |
| `ma.L1` ≈ −1 | Fazla fark alınmış; `d`'yi bir azalt |
| `ma.S.L12 = −0.9`, `D = 1` | Mevsim deseni çok kararlı |
| Yakın, ters işaretli `ar.L1` ve `ma.L1` | Birbirini götürüyor; ikisini de çıkar |

## Tahminin şekli

| Model | Uzun ufukta tahmin |
|---|---|
| `d = 0`, sabit var | Ortalamaya döner |
| `d = 1`, sabit yok | Düz: son düzeyde kalır |
| `d = 1`, sabit var | Doğru: sabit eğimle gider |
| `d = 2` | Doğru: son eğimle gider |
| `D = 1` | Son mevsimin desenini tekrarlar |
| `d = 1`, `D = 1` | Desen + son düzey; trend taşır |

Uzun ufukta tahmini AR ve MA terimleri değil, **fark ve sabit** belirler. AR ve
MA yalnızca ilk birkaç adımı biçimlendirir.

## Sabit ve trend

```python
ARIMA(train, order=(1, 0, 0))                # d = 0: sabit kendiliginden var
ARIMA(train, order=(0, 1, 1), trend="t")     # d = 1: kayma (dogrusal trend)
ARIMA(train, order=(1, 0, 0), trend="n")     # sabitsiz
```

`d ≥ 1` iken sabit kendiliğinden eklenmez; trend isteniyorsa `trend="t"`.

## Çarpımsal seri

```python
import numpy as np

fit = ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
forecast = np.exp(fit.forecast(12))
```

Hata ölçüleri **geri çevrilmiş** tahmin üzerinden hesaplanır, logaritma
üzerinden değil. Logaritmalı ve logaritmasız modellerin AIC'leri
karşılaştırılamaz (farklı veri).

## Hız

| Durum | Ne yapmalı |
|---|---|
| Uzun mevsim (`m = 365`) | ARIMA uygun değil; Fourier terimleri (Bölüm 18) |
| Çok sayıda kayan başlangıç | Küçük mertebe; gerekirse `train.iloc[-n:]` ile son `n` gözlem |
| Büyük `p`, `q` | Yavaş ve gereksiz; 2'nin altında tut |

Günlük, `m = 7`, bin gözlemlik seride küçük bir mevsimsel model yarım saniyenin
altında kuruluyor.

## `ARIMA` ve `SARIMAX`

`statsmodels.tsa.statespace.sarimax.SARIMAX` aynı modelin daha eski ve daha
ayrıntılı arayüzü. Başka kaynaklarda onu göreceksin; `order` ve
`seasonal_order` aynı anlamda. Dış değişken (`exog`) ikisinde de var.
