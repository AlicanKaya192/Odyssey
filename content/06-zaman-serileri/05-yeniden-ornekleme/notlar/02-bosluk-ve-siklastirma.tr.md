## Düzensiz seriyi ızgaraya oturtmak

```python
t = pd.read_csv("log.csv", index_col="time", parse_dates=True)["value"]

gaps = t.index.to_series().diff()
print(gaps.min(), gaps.median(), gaps.max())     # aralik dagilimi

grid = t.resample("h").mean()                     # duzenli izgara
counts = t.resample("h").count()                  # kovada kac kayit var
print(grid.isna().sum(), counts.min(), counts.max())
```

**Izgara aralığını nasıl seçersin:** ortanca aralığın birkaç katı. Kayıtlar
ortalama 7 dakikada bir geliyorsa saatlik ızgarada kova başına 8 civarı kayıt
olur ve ortalama sağlam çıkar. 5 dakikalık ızgarada kovaların yarısı boş
kalır.

## Boş kovayı doldurmak

| Yöntem | Ne yapıyor | Ne zaman |
|---|---|---|
| `ffill()` | Son bilinen değeri ileri taşıyor | Seviye: fiyat, stok, ayar değeri |
| `bfill()` | Sonraki değeri geri taşıyor | Nadiren; **geleceği kullanıyor** |
| `interpolate()` | İki uç arasında düz çizgi | Yavaş değişen ölçüm: sıcaklık |
| `interpolate(method="time")` | Zamana orantılı ara değer | İndeks eşit aralıklı değilse |
| `fillna(0)` | Sıfır yazıyor | Yalnızca "kayıt yok = sıfır" ise |
| Hiçbiri | `NaN` bırakıyor | Emin değilsen en dürüstü |

Hepsine **sınır** konabiliyor:

```python
grid.ffill(limit=2)            # en fazla 2 kova tasi
grid.interpolate(limit=3)      # en fazla 3 kova doldur
```

Sınır, uzun kesintileri boş bırakıyor. 5 saatlik kesintiyi düz çizgiyle
doldurmak, o beş saatte ne olduğunu bildiğini iddia etmek oluyor.

**`bfill` ve tahmin.** `bfill` bir satırı **sonraki** değerle dolduruyor.
Tahmin modeli kuracaksan bu sızıntı: o an bilinmeyen bir değer geçmişe
yazılıyor. Analiz için sorun değil, modelleme için tehlikeli.

## Sıklaştırma reçeteleri

**Toplamı paylaştırmak** (aylık → günlük):

```python
monthly = s.resample("MS").sum()
per_day = monthly / monthly.index.days_in_month
idx = pd.date_range(monthly.index[0], monthly.index[-1] + pd.offsets.MonthEnd(0), freq="D")
daily = per_day.reindex(idx, method="ffill")
```

Son ayın da tamamını kapsamak için indeks elle kuruluyor;
`monthly.resample("D")` son etikette duruyor.

**Seviyeyi taşımak** (haftalık fiyat → günlük):

```python
daily = weekly.resample("D").ffill()
```

**Ölçümü ara değerle doldurmak** (günlük sıcaklık → 6 saatlik):

```python
six_hourly = daily.resample("6h").interpolate()
```

## Sıklaştırmanın sınırı

| Elinde olan | Sıklaştırınca **kazanamadığın** |
|---|---|
| Aylık toplam | Haftanın günleri arasındaki fark |
| Günlük toplam | Günün saatleri arasındaki fark |
| Haftalık fiyat | Hafta içindeki iniş çıkış |

Sıklaştırılmış seri daha çok satır içeriyor ama **daha çok bilgi içermiyor.**
Onunla model eğitirsen model, sıklaştırma yönteminin kendisini öğreniyor
(düz çizgiyi, basamakları), gerçek deseni değil.

Ne zaman sıklaştırılır: iki seriyi aynı ızgarada birleştirmek gerektiğinde
(günlük satış + aylık bütçe) ve düşük sıklıktaki değer gerçekten o dönem
boyunca geçerliyse (aylık fiyat listesi, haftalık kampanya).

## Yaz saati ve günlük kovalar

Saat dilimli bir indekste `resample("D")` **yerel** güne göre kovalıyor. Yaz
saatine geçiş günü 23, çıkış günü 25 saat içeriyor:

```python
local = utc_series.tz_convert("Europe/Berlin")
print(local.resample("D").count())     # 24, 23, 24, ...
```

Günlük toplam o gün düşük, çıkış günü yüksek çıkıyor. Tüketimi karşılaştırırken
günlük **ortalamayı** kullanmak ya da o iki günü işaretlemek gerekiyor.
