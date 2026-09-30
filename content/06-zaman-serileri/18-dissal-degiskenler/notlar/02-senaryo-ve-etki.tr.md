Dış değişkenli bir model yalnızca tahmin vermez; iki soruyu daha cevaplar:
"bu olay ne kadar etkiledi?" ve "şunu yaparsak ne olur?"

## Reçete

1. **Değişkenleri listele** ve her biri için sor: tahmin anında hazır mı?
2. **Tabloyu kur:** eğitim için `X_train`, gelecek için `X_future`. Aynı
   sütunlar, aynı sıra, `NaN` yok.
3. **Önce değişkensiz modeli** sına (çıta).
4. **Değişkenleri ekle**, katsayılara bak: işareti ve boyu mantıklı mı?
5. **Kayan başlangıçla** sına; bilinmeyen değişkeni her deneyde o an bilinenle
   doldur.
6. **Tavanı ayrı raporla:** gerçek değerle bulunan sonuç.

## Gelecek tablosu

```python
future_index = pd.date_range(train.index[-1], periods=h + 1, freq="D")[1:]
future = pd.DataFrame(index=future_index)

future["promo"] = future_index.isin(planned_promo_days).astype(int)
future["holiday"] = future_index.isin(holiday_dates).astype(int)

normal = train["temp_c"].groupby(train.index.dayofyear).mean()
future["temp_c"] = [normal.get(day, normal.mean()) for day in future_index.dayofyear]

forecast = fit.forecast(h, exog=future[columns])
```

`normal.get(day, normal.mean())`: artık yılın 366. günü gibi eğitimde olmayan
bir gün için ortalamaya düşer.

## Katsayıyı denetlemek

| Soru | Nereye bak |
|---|---|
| İşareti beklediğim gibi mi? | `coef` |
| Sıfırdan ayırt edilebiliyor mu? | p-değeri ve güven aralığı |
| Boyu makul mü? | Kaba hesapla karşılaştır (aynı günün komşuları) |
| Kararlı mı? | Farklı eğitim dönemlerinde yeniden kur |
| Başka değişkenle mi karışıyor? | Birini çıkarıp ötekinin katsayısına bak |

Beklemediğin işaretli bir katsayı çoğu zaman bir **karıştırıcıya** işaret eder.
"Kampanya satışı düşürüyor" çıkıyorsa kampanyalar büyük olasılıkla zaten zayıf
dönemlerde yapılıyordur ve model o zayıflığı görmüyordur.

## Senaryo sormak

```python
with_promo = future[columns].copy()
without_promo = with_promo.copy()
without_promo["promo"] = 0

gain = fit.forecast(h, exog=with_promo) - fit.forecast(h, exog=without_promo)
print(round(gain.sum()))
```

Bu, modelin kampanyaya biçtiği toplam ek satış. İki uyarı:

- Model yalnızca **eğitimde gördüğü türden** kampanyaları bilir. Hiç
  denenmemiş bir süre ya da indirim oranı için söylediği bir uzatmadır.
- Katsayı bir **ilişki**; nedensellik iddiası için kampanya günlerinin nasıl
  seçildiğini bilmek gerekir. Kampanyalar rastgele günlere konmuşsa katsayı
  güvenilir; hep iyi günlere konmuşsa şişkindir.

## Geçmişteki bir olayın etkisi

"14 Mart'taki kampanya ne kadar getirdi?" sorusu için olay **olmasaydı**
ne olurdu tahminine ihtiyaç var:

1. Modeli olaydan önceki veriyle kur.
2. Olay günü için `promo = 0` ile tahmin et.
3. Gerçek − tahmin, olayın etkisi (artı tahmin hatası).

Bölüm 13'te aykırı günleri "bir hafta öncesi ile sonrasının ortalamasıyla"
onarmıştın; bu, aynı sorunun model gerektirmeyen kaba cevabıydı.

## Bilinmeyen değişkenin hatası nereye gider?

```text
satis tahmini hatasi  =  modelin kendi hatasi
                       +  katsayi x (degiskenin tahmin hatasi)
```

Kafede sıcaklık katsayısı 5.5. Mevsim normali sıcaklığı ortalama 2.2 derece
kaçırıyorsa bu, satış tahminine 5.5 × 2.2 ≈ 12 birimlik ek belirsizlik
getirir. Tavan ile gerçek sonuç arasındaki fark (9.4 ile 15.0) tam olarak bu.

Sonuç: bilinmeyen bir değişkeni eklemek ancak **tahmin edilebilir** kısmı
büyükse işe yarar. Sıcaklığın mevsimsel kısmı öngörülebilir; günlük oynaması
28 gün öncesinden öngörülemez.

## Değişken eklemeye değer mi?

Aynı kayan başlangıçta, değişkenli ve değişkensiz:

| Durum | Karar |
|---|---|
| Hata belirgin düşüyor, deneylerin çoğunda | Ekle |
| Yalnızca "gerçek değerle" düşüyor | Değişken iyi ama geleceği bilinmiyor; daha iyi bir vekil ara |
| Hata değişmiyor | Ekleme; bakımı maliyet |
| Ortalama düşüyor, en kötü deney büyüyor | Dikkat: değişken bazı dönemlerde yanıltıyor |

## Bakım

- Tatil listesi ve kampanya takvimi **her yıl güncellenir**; eksik bir tatil,
  modelin o günü sıradan sanması demek.
- Yeni bir olay türü çıktıysa (yeni bir indirim günü) ilk yıl modelde yoktur;
  elle düzeltme ya da benzer bir olayın katsayısı gerekir.
- Katsayıları dönem dönem yeniden tahmin et ve izle: kayan bir katsayı, etkinin
  değiştiğini söyler.
