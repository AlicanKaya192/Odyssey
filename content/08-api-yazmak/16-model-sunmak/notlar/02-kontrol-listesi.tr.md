Bir modeli API ile yayına almadan önce bak.

## Yükleme

- ☐ Model `lifespan`'da **bir kez** yükleniyor, uç noktada değil.
- ☐ Kaydedilen şey bütün hat (Pipeline), yalnızca model değil.
- ☐ scikit-learn sürümü `requirements.txt`'te sabit.

## Girdi

- ☐ Her özellik Pydantic modelinde, tipi ve mantıklı aralığıyla
  (`Field(gt=0, le=10)`).
- ☐ Sütun sırası eğitimdekiyle aynı (bir yardımcı işlevde, tek yerde).
- ☐ Toplu tahminde liste boyutuna sınır var (`if len(flowers) > 100:`
  → hata): biri 10 milyon satır göndermesin.

## Çıktı

- ☐ NumPy değerleri `int()`, `float()`, `.tolist()` ile çevrildi.
- ☐ Sınıf numarası yerine okunur ad (`"setosa"`), gerekirse olasılık.
- ☐ `/model` uç noktası: model türü, sürümü, sınıflar.

## Davranış

- ☐ Tahmin uç noktası `def` (scikit-learn bekleten bir hesap yapar;
  `async def` içinde olay döngüsünü kilitler).
- ☐ Testler: bilinen birkaç örnek doğru sınıfı alıyor, bozuk girdi `422`.

## Yaygın hatalar (ölçülenler)

| Hata | Sonuç |
|---|---|
| NumPy değerini doğrudan döndürmek | `500` |
| Ölçekleyiciyi unutmak | Hata yok, her tahmin aynı sınıf |
| Tek örneği düz liste vermek (`[5.1, 3.5, ...]`) | scikit-learn `Expected 2D array` |
