Hangi ölçüyü ne zaman kullanacağın, tek bir soruya bakıyor: **bu problemde
büyük bir hata, küçük hataların toplamından daha mı pahalı?**

## Karşılaştırma tablosu

| Ölçü | Birimi | Büyük hataya tepkisi | Aykırı değere | Okunabilirlik |
|---|---|---|---|---|
| MAE | Hedefin birimi | Orantılı | Dayanıklı | Yüksek |
| MSE | Birimin karesi | Orantısız (kare) | Hassas | Düşük |
| RMSE | Hedefin birimi | Orantısız (kare) | Hassas | Orta |
| R² | Yok | Orantısız (kare tabanlı) | Hassas | Orta |
| MAPE | Yüzde | Orantılı | Dayanıklı | Yüksek |

## Karar soruları

**1. Tek bir büyük hata felaket mi?**

- Evet → **RMSE**. Uçuş süresi, ilaç dozu, kritik stok seviyesi.
- Hayır → **MAE**. Toplam maliyet, günlük satış ortalaması.

**2. Sonucu teknik olmayan birine anlatacak mısın?**

- Evet → **MAE** ya da **MAPE**. "Ortalama 18 bin lira yanılıyoruz."
- Hayır → R² de eklenebilir.

**3. İki farklı problemi karşılaştıracak mısın?**

- Evet → **R²**. Birimsiz olduğu için tek karşılaştırılabilir ölçü.
- Hayır → Birimli ölçüler daha bilgilendirici.

**4. Hedefte sıfır ya da sıfıra çok yakın değerler var mı?**

- Evet → **MAPE kullanma.** Bölme patlıyor ya da yüzde uçuyor.
- Hayır → MAPE bir seçenek.

**5. Hedefin ölçeği kayıtlar arasında çok değişiyor mu?**
(10 birimlik de var, 10.000 birimlik de)

- Evet → **MAPE** ya da logaritmik dönüşüm. MAE büyük kayıtların
  hatasıyla dolup taşıyor.
- Hayır → MAE / RMSE yeterli.

## Kod karşılıkları

```python
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score,
)

mae = mean_absolute_error(y_test, prediction)
mse = mean_squared_error(y_test, prediction)
rmse = mse ** 0.5
mape = mean_absolute_percentage_error(y_test, prediction)
r2 = r2_score(y_test, prediction)
```

`mean_absolute_percentage_error` **oran** döndürüyor (0.08), yüzde değil.
Yüzdeye çevirmek için 100 ile çarpılıyor.

## Elle hesaplama

Formülleri bilmek, hata mesajı okumaktan daha çok işe yarıyor.

```python
errors = [a - p for a, p in zip(actual, predicted)]
n = len(errors)

mae = sum(abs(e) for e in errors) / n
mse = sum(e ** 2 for e in errors) / n
rmse = mse ** 0.5

mean = sum(actual) / n
ss_res = sum(e ** 2 for e in errors)
ss_tot = sum((a - mean) ** 2 for a in actual)
r2 = 1 - ss_res / ss_tot
```

`ss_res` modelin hatası, `ss_tot` taban çizginin hatası. R² ikisinin
oranından geliyor — **taban çizgi ölçünün içine gömülü.**

## Aynı sonucun farklı görünüşleri

Aşağıdaki dördü aynı modelin aynı tahminlerini anlatıyor:

```
MAE   18.50
RMSE  22.86
R²     0.943
MAPE   0.063
```

Hiçbiri ötekinden "doğru" değil. Farklı sorulara cevap veriyorlar:

- MAE: ne kadar yanılıyorum?
- RMSE: büyük hatalarım var mı?
- R²: taban çizgiye göre neredeyim?
- MAPE: oransal olarak ne kadar yanılıyorum?

**RMSE her zaman MAE'den büyük ya da ona eşit.** Aralarındaki fark
büyükse, birkaç büyük hata var demektir. Bu iki sayıyı birlikte yazmanın
sebebi de bu: farkın kendisi bilgi taşıyor.

## Sık yapılan hatalar

- **`mean_squared_error`'ı RMSE sanmak.** sklearn kareyi döndürüyor;
  karekökünü sen alıyorsun.
- **Argümanları ters yazmak.** Sıra her zaman `(gerçek, tahmin)`. MAE
  affediyor, R² affetmiyor.
- **Farklı test kümelerinden gelen sayıları karşılaştırmak.** İki modelin
  MAE'si ancak **aynı ayrımda** ölçülmüşse karşılaştırılabiliyor.
- **Sınıflandırmada regresyon ölçüsü kullanmak.** Hedef kategoriyse MAE
  anlamsız; oraya accuracy, precision, recall giriyor.
