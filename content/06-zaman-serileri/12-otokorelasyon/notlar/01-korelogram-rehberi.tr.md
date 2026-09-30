## Çağrılar

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, pacf

values = acf(x, nlags=20)            # dizi: values[0] = 1, values[k] = gecikme k
values = pacf(x, nlags=20)

fig = plot_acf(x, lags=20)           # korelogram, bant dahil
fig = plot_pacf(x, lags=20)
fig = plot_acf(x, lags=20, zero=False)   # gecikme 0 cubugunu gizle

table = acorr_ljungbox(x, lags=[10, 20])   # sutunlar: lb_stat, lb_pvalue
```

`x` içinde `NaN` olmamalı. Fark aldıysan `dropna()`.

## Güven bandı

$$\pm \frac{1.96}{\sqrt{n}}$$

| Gözlem sayısı | Bant |
|---|---|
| 50 | ±0.277 |
| 100 | ±0.196 |
| 250 | ±0.124 |
| 500 | ±0.088 |
| 1000 | ±0.062 |
| 5000 | ±0.028 |

`plot_acf`'in çizdiği bant gecikme arttıkça biraz **genişler** (önceki
gecikmelerdeki korelasyonu hesaba katıyor); sabit ±1.96/√n iyi bir ilk
yaklaşım.

Çok uzun seride bant çok dar: 0.05'lik bir korelasyon "anlamlı" çıkar ama
pratikte işe yaramaz. **Anlamlı** ile **büyük** aynı şey değil.

## Kaç gecikme?

- Mevsim varsa en az iki tur: günlük veride 14–21, aylıkta 24–36, saatlikte
  48 ve 336.
- Üst sınır: gözlem sayısının dörtte biri. Uzak gecikmeler az sayıda çiftle
  hesaplanıyor ve güvenilmez.

## Şekilden teşhise

| ACF'de ne görüyorsun | Ne demek | Ne yap |
|---|---|---|
| Hepsi yüksek, çok yavaş sönüyor | Trend / rastgele yürüyüş | `diff()` |
| `m`, `2m`, `3m`'de yavaş sönen tepeler | Güçlü mevsim | `diff(m)` |
| İlk birkaç gecikme yüksek, hızla sönüyor | Kısa hafıza (AR tipi) | PACF'ye bak |
| Yalnızca 1. (ya da ilk `q`) gecikme bandın dışında | MA tipi | `q` o sayı |
| Dalgalanarak, işaret değiştirerek sönüyor | AR, eksi katsayılı ya da AR(2) | PACF'ye bak |
| 1. gecikme −0.5 civarı, gerisi sıfır | Fazla fark alınmış | Bir farkı geri al |
| Mevsimsel farktan sonra yalnızca `m`'de eksi çubuk | Mevsimsel MA terimi | Bölüm 17: `Q = 1` |
| Hepsi bandın içinde | Beyaz gürültü | Modellenecek hafıza yok |

## ACF ve PACF birlikte

| ACF | PACF | Süreç |
|---|---|---|
| Yavaşça sönüyor | `p`. gecikmeden sonra kesiliyor | AR(p) |
| `q`. gecikmeden sonra kesiliyor | Yavaşça sönüyor | MA(q) |
| Yavaşça sönüyor | Yavaşça sönüyor | İkisi birden: ARMA |
| Hepsi bantta | Hepsi bantta | Beyaz gürültü |

"Kesiliyor": o gecikmeden sonraki bütün çubuklar bandın içinde. "Sönüyor":
çubuklar adım adım küçülüyor.

Gerçek veride şekiller ders kitabındaki kadar temiz olmaz. ACF ve PACF **aday**
verir; son kararı modelleri karşılaştırarak verirsin (Bölüm 15 ve 17).

## Ljung–Box

```python
acorr_ljungbox(x, lags=[10])
```

| | |
|---|---|
| Varsayım | İlk `m` gecikmenin otokorelasyonu sıfır (beyaz gürültü) |
| Küçük p (< 0.05) | Hafıza var: modellenebilir yapı kalmış |
| Büyük p | Hafıza bulunamadı |
| `lags` seçimi | Mevsimsiz 10; mevsimli `2m` (günlükte 14, aylıkta 24) |

Bir modelin kalıntısına uygularken `model_df` argümanına modelin parametre
sayısını verirsin; test serbestlik derecesini ona göre düzeltir (Bölüm 17).

## Otokorelasyonun başka kullanımları

- **Periyot bulmak:** ACF'nin ilk büyük tepesi mevsimin boyu.
- **Özellik seçmek:** makine öğrenmesi modeline (Bölüm 19) hangi gecikmeleri
  vereceğini ACF ve PACF söyler: bandı aşanları.
- **Kalıntı denetimi:** her modelden sonra.
- **Örnekleme sıklığı:** 1. gecikme 0.99 ise ardışık gözlemler neredeyse aynı
  bilgiyi taşıyor; daha seyrek örneklemek bilgi kaybettirmez.
