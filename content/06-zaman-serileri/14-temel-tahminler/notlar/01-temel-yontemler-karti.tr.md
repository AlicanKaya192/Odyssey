## Dört yöntem, tek bakışta

Gösterim: eğitim verisi $y_1, \dots, y_T$; ufuk $h$; mevsim boyu $m$.

| Yöntem | Tahmin | Ne zaman iyi | Zayıf yanı |
|---|---|---|---|
| Ortalama | Eğitim ortalaması | Trendsiz, mevsimsiz, durağan seri | Trendde düzeyi kaçırır |
| Naif | $y_T$ | Rastgele yürüyüş: fiyat, kur | Mevsimi yok sayar; son gün aykırıysa felaket |
| Mevsimsel naif | Bir önceki mevsimin aynı konumu | Güçlü, kararlı mevsim | Trendi bir mevsim geriden izler |
| Kayma | $y_T + h \cdot \dfrac{y_T - y_1}{T - 1}$ | Düzgün, doğrusal trend | Yalnızca iki noktaya bakar |

## Genel işlevler

```python
import numpy as np
import pandas as pd


def future_index(train, h):
    return pd.date_range(train.index[-1], periods=h + 1, freq=train.index.freq)[1:]


def mean_forecast(train, h):
    return pd.Series(train.mean(), index=future_index(train, h))


def naive_forecast(train, h):
    return pd.Series(train.iloc[-1], index=future_index(train, h))


def seasonal_naive(train, h, m):
    last = train.iloc[-m:].to_numpy()
    return pd.Series([last[i % m] for i in range(h)], index=future_index(train, h))


def drift_forecast(train, h):
    slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
    steps = np.arange(1, h + 1)
    return pd.Series(train.iloc[-1] + slope * steps, index=future_index(train, h))
```

`train.index.freq` dolu olmalı: dosyayı okuduktan sonra `asfreq("D")` ya da
`asfreq("MS")`. `date_range(..., periods=h + 1)[1:]` son eğitim gününden
**sonraki** `h` tarihi veriyor ve her sıklıkta çalışıyor.

## Daha iyi temel yöntemler

Dört klasik yöntemin küçük düzeltmeleri çoğu zaman belirgin fark yaratır:

| Yöntem | Fikir | Kod |
|---|---|---|
| Son `k` ortalaması | Naifin gürültüye dayanıklı hâli | `train.iloc[-k:].mean()` |
| Son `k` mevsimin ortalaması | Mevsimsel naifin gürültüye dayanıklı hâli | Son `k * m` değeri `(k, m)` biçimine sok, sütun ortalaması al |
| Mevsimsel naif + kayma | Mevsim + doğrusal trend | Her tura `slope * m` ekle |
| Mevsimsel naif × büyüme | Mevsim + yüzdeyle büyüme | Geçen mevsimi büyüme oranıyla çarp |
| Ortanca | Aykırı günlere dayanıklı ortalama | `train.iloc[-k:].median()` |

Son `k` mevsimin ortalaması:

```python
def seasonal_mean(train, h, m, k=4):
    block = train.iloc[-k * m:].to_numpy().reshape(k, m)
    pattern = block.mean(axis=0)
    return pd.Series([pattern[i % m] for i in range(h)], index=future_index(train, h))
```

Tek bir haftayı kopyalamak o haftanın gürültüsünü de kopyalar; dört haftanın
ortalaması gürültüyü azaltır ama trende daha geç tepki verir.

## Tek adımlı kurulum

Bütün geçmiş için "her gün yarını tahmin et":

| Yöntem | Kod |
|---|---|
| Naif | `s.shift(1)` |
| Mevsimsel naif | `s.shift(m)` |
| Son `k` ortalaması | `s.shift(1).rolling(k).mean()` |
| Geçmişin tamamının ortalaması | `s.shift(1).expanding().mean()` |
| Son 4 mevsimin ortalaması | `sum(s.shift(m * i) for i in range(1, 5)) / 4` |

Hepsinde ortak olan: tahmin, tahmin ettiği günü **içermiyor**.

## Hangi seriye hangi çıta

```text
Mevsim var mi?
  hayir -> Trend / surukleme var mi?
             hayir -> ortalama ya da son k ortalamasi
             evet  -> naif; trend duzgunse kayma
  evet  -> Trend var mi?
             hayir -> mevsimsel naif ya da son k mevsimin ortalamasi
             evet  -> mevsimsel naif x buyume (carpimsal)
                      mevsimsel naif + kayma (toplamsal)
```

Emin değilsen hepsini hesapla ve en iyisini çıta yap: bir tablo, birkaç satır
kod.

## Temel yöntem ne zaman yeter

- Seri çok kısaysa (iki mevsimden az): karmaşık modeli besleyecek veri yok.
- Yüzlerce seriyi birden tahmin ediyorsan ve her birine emek ayıramıyorsan.
- Karar hataya duyarlı değilse (kabaca bir sipariş miktarı).
- Karmaşık modelin becerisi 0.05–0.10'un altındaysa: bakım maliyetine değmez.

Gerçek tahmin yarışmalarında mevsimsel naif ve basit üstel düzleştirme, çok
daha karmaşık yöntemlerin önemli bir kısmını geride bırakmıştır. Basit yöntemi
küçümseme; onu yenmek gerekiyor.
