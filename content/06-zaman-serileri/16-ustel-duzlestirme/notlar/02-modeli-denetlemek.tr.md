Bir model kurdun ve hatası çıtanın altında. Kullanmadan önce üç denetim daha.

## 1. Kalıntıda hafıza kaldı mı?

İyi bir model öngörülebilir olan her şeyi alır; geriye beyaz gürültü kalır
(Bölüm 12).

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

resid = fit.resid
print(acf(resid, nlags=14).round(2).tolist()[1:])
print(acorr_ljungbox(resid, lags=[14]))
```

| Kalıntının ACF'sinde | Anlamı | Ne yap |
|---|---|---|
| Hepsi bantta | Model hafızayı almış | Devam |
| 1. gecikme belirgin | Kısa dönem bağımlılık kalmış | ARIMA (Bölüm 17) |
| Mevsim gecikmesi (7, 12) belirgin | Mevsim tam alınmamış | `seasonal`'ı ve `seasonal_periods`'u denetle |
| Yavaş sönen, hepsi artı | Trend alınmamış | `trend` ekle |

Günlük satışın Holt–Winters kalıntısında Ljung–Box testi hâlâ küçük bir
p-değeri verir: model düzeyi ve mevsimi alıyor, günler arası kısa hafızayı
almıyor. Üstel düzleştirmenin doğal sınırı bu.

## 2. Kalıntı yanlı mı, düzensiz mi?

```python
print(round(resid.mean(), 2))                                 # sifira yakin olmali
print(resid.abs().groupby(resid.index.year).mean().round(1))  # yildan yila benzer mi
print(resid.abs().sort_values(ascending=False).head(5))       # en buyuk iskalar
```

- Ortalama sıfırdan uzaksa model sistematik olarak kayık.
- Kalıntının boyu yıllar içinde büyüyorsa toplamsal yerine çarpımsal mevsim
  gerekiyor.
- En büyük ıskalar hep aynı tarihlerdeyse (yılbaşı, bayram) takvim bilgisi
  eksik.

## 3. Katsayılar makul mü?

| Durum | Yorum |
|---|---|
| `α ≈ 1` | Model naife dönmüş; düzleştirecek bir şey yok |
| `α ≈ 0`, trend yok | Model ortalamaya dönmüş; seri bir sabitin etrafında |
| `β ≈ 0` | Eğim sabit: baştaki eğim hiç güncellenmiyor |
| `β` büyük | Eğim her sürprizle değişiyor; uzun ufukta tehlikeli |
| `γ ≈ 0` | Mevsim payları sabit; klasik ayrıştırmaya yakın |
| `γ` büyük | Mevsim payları geçen turun gürültüsünü kopyalıyor |
| `φ < 0.8` | Trend çok çabuk sönüyor; trend bileşeni gereksiz olabilir |

Katsayıların sınıra (0 ya da 1) yapışması hata değil; bir bulgu. Ama kısa
seride sınıra yapışan katsayı çoğu zaman "veri yetmedi" demek.

## Eğitim hatası ve test hatası

```python
train_mae = fit.resid.abs().mean()
test_mae = (test - fit.forecast(len(test))).abs().mean()
```

Test hatası doğal olarak daha büyük: eğitim hatası **bir adımlık**, test hatası
**çok adımlı**. Ama test hatası eğitim hatasının birçok katıysa model
ezberlemiş ya da test dönemi eğitimden farklı bir rejimde.

Yolcu modelinde eğitim hatası 2.6, test hatası 6.5: makul. Çarpımsal mevsimli
satış modelinde tek ayrımda 8.9 çıkıp 13 deneyde 15.5 çıkması ise bir uyarıydı:
tek ayrım iyimserdi.

## Hangi model, hangi seri

```text
Mevsim var mi?
  hayir -> Trend var mi?
             hayir -> basit ustel duzlestirme
             evet  -> Holt; uzun ufukta sonumlu
  evet  -> Dalgalar duzeyle buyuyor mu?
             hayir -> seasonal="add"
             evet  -> seasonal="mul"
           Trend var mi?
             belirsiz -> trendsiz ve trendli iki adayi kayan baslangicla karsilastir
```

Emin olmadığın her kararda iki adayı Bölüm 15'in düzeneğinden geçir. Berabere
kalırlarsa **az bileşenli** olanı seç: bakımı kolay, en kötü durumu daha iyi.

## Üretimde

- Model **yeniden eğitilir**: yeni veri geldikçe (günlük ya da haftalık)
  baştan `fit`. Üstel düzleştirme hızlı; bu bir sorun değil.
- Son kullanım için doğrulama ve test dahil **bütün veriyle** eğit.
- Tahminle birlikte temel yöntemin tahminini de sakla; model bozulursa (beceri
  sıfırın altına inerse) ilk oradan görünür.
- Aykırı günleri eğitimden önce düzelt (Bölüm 13): tek bir sıçrama, büyük `α`
  ile düzeyi günlerce yukarıda tutar.
