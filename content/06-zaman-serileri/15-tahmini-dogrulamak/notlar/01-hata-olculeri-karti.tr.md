Gösterim: gerçek $y_t$, tahmin $\hat{y}_t$, hata $e_t = y_t - \hat{y}_t$, test
uzunluğu $n$.

## Formüller

$$\text{MAE} = \frac{1}{n}\sum \lvert e_t \rvert$$

$$\text{RMSE} = \sqrt{\frac{1}{n}\sum e_t^2}$$

$$\text{MAPE} = \frac{100}{n}\sum \left\lvert \frac{e_t}{y_t} \right\rvert$$

$$\text{sMAPE} = \frac{100}{n}\sum \frac{2\,\lvert e_t \rvert}{\lvert y_t \rvert + \lvert \hat{y}_t \rvert}$$

$$\text{MASE} = \frac{\text{MAE}}{\dfrac{1}{T-m}\sum_{t=m+1}^{T} \lvert y_t - y_{t-m} \rvert}$$

MASE'nin paydası **eğitim** verisinden: her değerin bir mevsim öncekinden
mutlak farkının ortalaması. Mevsimi olmayan seride $m = 1$.

## Hangisi ne zaman

| Ölçü | Birim | Güçlü yanı | Zayıf yanı | Ne zaman |
|---|---|---|---|---|
| MAE | Serinin birimi | Okunaklı; aykırı değere dayanıklı | Seriler arası karşılaştırılamaz | Tek seri, günlük raporlama |
| RMSE | Serinin birimi | Büyük hatayı öne çıkarır | Birkaç gün bütün notu belirler | Büyük ıska pahalıysa |
| MAPE | Yüzde | Herkes anlar | Sıfırda tanımsız; asimetrik | Hep artı, sıfırdan uzak seri |
| sMAPE | Yüzde | 0–200 arasında sınırlı | Hâlâ sıfıra duyarlı; yorumu zor | Yarışma ölçüsü olarak |
| MASE | Birimsiz | Her seride tanımlı; çıtası belli | Açıklaması zahmetli | Çok seri, sıfırlı seri |
| Yanlılık | Serinin birimi | Yönü gösterir | Büyüklüğü göstermez | Her zaman, MAE'nin yanında |

Hangi ölçüyle seçersen model **o ölçüyü** iyileştirmeye çalışır:

- MAE'yi en küçük yapan tahmin **ortanca**dır.
- RMSE'yi en küçük yapan tahmin **ortalama**dır.
- MAPE'yi en küçük yapan tahmin ortancanın **altında** kalır.

Çarpık dağılımlı bir seride (çoğu gün az, arada bir çok satış) bu üçü farklı
tahminler ister. Ölçüyü karara göre seç, alışkanlığa göre değil.

## Kod

```python
import numpy as np


def mae(actual, forecast):
    return np.mean(np.abs(actual - forecast))


def rmse(actual, forecast):
    return np.sqrt(np.mean((actual - forecast) ** 2))


def bias(actual, forecast):
    return np.mean(actual - forecast)


def mape(actual, forecast):
    return np.mean(np.abs(actual - forecast) / np.abs(actual)) * 100


def smape(actual, forecast):
    total = np.abs(actual) + np.abs(forecast)
    return np.mean(2 * np.abs(actual - forecast) / total) * 100


def mase(actual, forecast, train, m=1):
    scale = np.mean(np.abs(train[m:] - train[:-m]))
    return mae(actual, forecast) / scale
```

Hepsi numpy dizisi bekliyor: `test.to_numpy()`. İki pandas serisini doğrudan
çıkarırsan **indekse göre** hizalanır; indeksleri farklıysa sonuç `NaN` dolar.

scikit-learn'de hazırları: `mean_absolute_error`, `root_mean_squared_error`,
`mean_absolute_percentage_error` (yüzde değil **oran** döndürür: 0.035).

## MASE'yi okumak

| MASE | Anlamı |
|---|---|
| 0.5 | Tek adımlı mevsimsel naifin yarısı kadar hata |
| 1.0 | Onunla aynı |
| 2.0 | İki katı |

Payda **tek adımlı** hata. Çok adımlı bir tahminin MASE'si 1'in üstünde
çıkabilir ve bu kötü olduğu anlamına gelmez: uzak ufuk zaten daha zor. Aynı
ufuktaki iki yöntemi kendi aralarında karşılaştır.

## Ağırlıklı yüzde hata

Çok sayıda seriyi (yüzlerce ürün) tek sayıyla özetlerken MAPE'nin yerine sık
kullanılan ölçü:

$$\text{WAPE} = \frac{\sum \lvert e_t \rvert}{\sum \lvert y_t \rvert} \times 100$$

Toplam mutlak hata bölü toplam gerçek değer. Sıfırlı günler paydayı bozmaz ve
büyük hacimli günler daha çok ağırlık alır. Perakendede standart.

## Raporda neler olmalı

1. Ölçü ve birimi.
2. Ufuk.
3. Kaç deney, hangi dönem.
4. Ortalama **ve** yayılım (standart sapma ya da en iyi / en kötü).
5. Temel yöntemin aynı düzenekteki sonucu.
6. Yanlılık.

"MAE 17.2 (13 deney, 28 günlük ufuk, 2024; en kötü 39.8); mevsimsel naif 17.9;
yanlılık +1.7" tam bir cümle. "Hata 12" değil.
