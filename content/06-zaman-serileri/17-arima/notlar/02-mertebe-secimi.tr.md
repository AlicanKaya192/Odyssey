## Reçete

1. **Çiz.** Trend, mevsim, büyüyen dalga, aykırı günler, seviye kayması.
2. **Dönüştür.** Dalga büyüyorsa logaritma. Aykırı günleri düzelt (Bölüm 13).
3. **Fark.** Mevsim varsa `D = 1`; hâlâ kayma varsa `d = 1`. Standart sapma
   yükseldiyse geri al (Bölüm 11).
4. **ACF ve PACF.** Farkı alınmış seride (Bölüm 12).
5. **Adaylar.** İki üç küçük model.
6. **AIC.** En küçüğü; yakın olanlardan en az katsayılı olanı.
7. **Kalıntı.** Ljung–Box, ACF, en büyük ıskalar.
8. **Sınama.** Kayan başlangıç; temel yönteme ve öteki modellere karşı.

## ACF ve PACF'den adaya

Farkı alınmış serinin korelogramında:

| Ne görüyorsun | Aday |
|---|---|
| PACF 1'den sonra kesiliyor, ACF sönüyor | `p = 1` |
| PACF 2'den sonra kesiliyor | `p = 2` |
| ACF 1'den sonra kesiliyor, PACF sönüyor | `q = 1` |
| İkisi de sönüyor | `p = 1`, `q = 1` |
| İkisi de bantta | `p = 0`, `q = 0` |
| ACF'de yalnızca `m`'de eksi çubuk | `Q = 1` |
| ACF'de `m`, `2m`, `3m`'de sönen çubuklar; PACF'de yalnızca `m`'de | `P = 1` |
| 1. gecikmede −0.5 civarı, `d = 1` sonrası | `q = 1` (ya da fazla fark) |

Mevsimsel farktan sonra en sık çıkan sonuç `Q = 1`, `P = 0`.

## Küçük bir arama

Adayları elle yazmak yerine küçük bir ızgara:

```python
import itertools
import warnings

warnings.simplefilter("ignore")

rows = []
for p, q in itertools.product(range(3), range(3)):
    fit = ARIMA(train, order=(p, 1, q), seasonal_order=(0, 1, 1, 7)).fit()
    rows.append({"order": (p, 1, q), "aic": fit.aic, "terms": p + q})

table = pd.DataFrame(rows).sort_values("aic")
print(table.head(5))
```

- `d` ve `D` ızgaraya **girmez**: farklı farkla AIC karşılaştırılamaz.
- En iyi birkaç satırın AIC'si birbirine çok yakındır (2 puanın altı):
  aralarından **en az terimli** olanı seç.
- Izgara bir ön eleme. Son karar kalıntıda ve kayan başlangıçta.

## AIC ve BIC

| | AIC | BIC |
|---|---|---|
| Ceza | Katsayı başına 2 | Katsayı başına `ln(n)` |
| Eğilimi | Biraz büyük modeller | Küçük modeller |
| Ne zaman | Amaç tahminse | Amaç "doğru" yapıyı bulmaksa |

İkisi de **göreli**: tek başına bir AIC değeri bir şey söylemez. Eksi olabilir;
daha küçük (daha eksi) olan iyi.

Fark ne kadar olmalı?

| AIC farkı | Yorum |
|---|---|
| 0–2 | Ayırt edilemez; basit olanı seç |
| 2–10 | Küçük olan daha iyi, ama kesin değil |
| 10'dan çok | Açık fark |

## Kalıntı denetimi

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

skip = d + D * m                       # baslangic etkisi
resid = fit.resid.iloc[skip:]

print(round(resid.mean(), 2))
print(acf(resid, nlags=2 * m).round(2).tolist()[1:])
print(acorr_ljungbox(resid, lags=[2 * m], model_df=p + q + P + Q))
```

- **İlk değerleri at.** Fark alan modelde ilk `d + D × m` kalıntı modelin
  başlangıcından gelir ve çok büyüktür; testi bozar.
- **`model_df`:** modelin katsayı sayısı. Test, serbestlik derecesini ona göre
  düzeltir.
- **p > 0.05:** hafıza kalmamış.

| Kalıntıda | Ne yap |
|---|---|
| 1. gecikme bandın dışında | `p` ya da `q`'yu bir artır |
| `m`. gecikme bandın dışında | `P` ya da `Q`'yu bir artır |
| Yavaş sönen artı çubuklar | `d`'yi artır |
| Genişlik zamanla büyüyor | Logaritma |
| Birkaç dev değer | Aykırı günler; Bölüm 13 |
| Hep aynı tarihlerde ıska | Takvim; Bölüm 18 |

## Fazla modelin belirtileri

- Bir katsayının p-değeri 0.05'in üstünde.
- AR ve MA katsayıları yakın, ters işaretli.
- Katsayı ±1'e yapışmış.
- Terim ekleyince AIC 2'den az düşüyor.
- Uyarılar: yakınsama sağlanamadı, tersinemez başlangıç değerleri.
- Eğitim hatası düşerken kayan başlangıç hatası yükseliyor.

Birini görürsen bir terim **çıkar** ve yeniden bak.

## AIC ile test hatası çelişirse

Olur; dersteki (1,0,0)(0,1,1)₇ örneği gibi. Üç olası neden:

1. **Model yanlış kurulmuş** ama bir adımlık uyumu iyi (örneğin gereken fark
   alınmamış). Kalıntı testi bunu yakalar.
2. **Ufuk farkı.** AIC bir adımlık uyumu ölçer; sen 28 adım ileriyi
   kullanıyorsun. Uzun ufukta farkın ve sabitin etkisi büyür.
3. **Şans.** Tek ayrım. Kayan başlangıca bak.

Kural: AIC **eler**, kayan başlangıç **seçer**.
