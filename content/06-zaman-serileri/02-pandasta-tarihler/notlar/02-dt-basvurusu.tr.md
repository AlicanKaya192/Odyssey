Hepsi bir tarih sütununda `sutun.dt.<ad>` diye kullanılıyor. Tek bir
`Timestamp`'te aynı adlar `.dt` olmadan çalışıyor (`t.year`).

## Parçalar

| Ad | Verdiği | `2024-03-09 14:37` için |
|---|---|---|
| `year` | Yıl | `2024` |
| `quarter` | Çeyrek (1–4) | `1` |
| `month` | Ay (1–12) | `3` |
| `day` | Ayın günü | `9` |
| `hour`, `minute`, `second` | Saat parçaları | `14`, `37`, `0` |
| `dayofweek` | Haftanın günü, pazartesi 0 | `5` |
| `dayofyear` | Yılın kaçıncı günü | `69` |
| `day_name()` | Günün adı | `Saturday` |
| `month_name()` | Ayın adı | `March` |
| `days_in_month` | Ayın gün sayısı | `31` |
| `date` | Yalnızca gün (Python `date`) | `2024-03-09` |
| `time` | Yalnızca saat | `14:37:00` |

`isocalendar()` tek değer değil, üç sütunlu bir tablo veriyor: `year`,
`week`, `day`. Yıl sonu tuzağı için ikisini birlikte al:

```python
iso = df["date"].dt.isocalendar()
df["week_label"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
```

## Evet / hayır soruları

| Ad | Anlamı |
|---|---|
| `is_month_start`, `is_month_end` | Ayın ilk / son günü mü |
| `is_quarter_start`, `is_quarter_end` | Çeyreğin ilk / son günü mü |
| `is_year_start`, `is_year_end` | Yılın ilk / son günü mü |
| `is_leap_year` | Artık yıl mı |

Hafta sonu için hazır bir ad yok: `df["date"].dt.dayofweek >= 5`.

## Yuvarlamak

| İşlem | Ne yapıyor | `14:37` için |
|---|---|---|
| `normalize()` | Saati gece yarısına çekiyor | `00:00` |
| `floor("h")` | Aşağı yuvarlıyor | `14:00` |
| `ceil("h")` | Yukarı yuvarlıyor | `15:00` |
| `round("15min")` | En yakına yuvarlıyor | `14:30` |

Sık kullanılan birimler: `"D"` gün, `"h"` saat, `"min"` dakika, `"s"` saniye.
Ay ve yıl sabit uzunlukta olmadığı için `floor("M")` yok; ayın başı için
`dt.to_period("M").dt.start_time` (Bölüm 04).

## Süre sütunu (`timedelta64`)

```python
gap = df["end"] - df["start"]

gap.dt.days                # tam gun
gap.dt.total_seconds()     # toplam saniye
gap.dt.total_seconds() / 3600   # saat
gap / pd.Timedelta(hours=1)     # saat (ayni sey)
gap > pd.Timedelta(days=3)      # sureyle karsilastirma
```

Elle süre kurmak: `pd.Timedelta("2h 15min")`, `pd.Timedelta(days=3)`,
`pd.to_timedelta(df["minutes"], unit="min")`.

## Saat dilimi işlemleri

| İşlem | Ne zaman | Saat değişiyor mu |
|---|---|---|
| `dt.tz_localize("Europe/Istanbul")` | Dilimsiz sütuna dilimini **tanıtmak** | Hayır |
| `dt.tz_convert("UTC")` | Dilimli sütunu başka dilime **dönüştürmek** | Evet, an aynı |
| `dt.tz_localize(None)` | Dilimi atıp dilimsiz yapmak | Hayır |
| `pd.to_datetime(..., utc=True)` | Okurken doğrudan UTC | — |

Yaz saati için `tz_localize` seçenekleri:

| Parametre | Durum | Değerler |
|---|---|---|
| `nonexistent=` | Baharda atlanan saat | `"shift_forward"`, `"shift_backward"`, `"NaT"`, `"raise"` |
| `ambiguous=` | Sonbaharda iki kez yaşanan saat | `"NaT"`, `"raise"`, ya da `True`/`False` dizisi |

Dilimli bir sütundan yerel günü almak: `dt.tz_convert(...).dt.date`. Önce
dönüştür, sonra günü al; UTC günü ile yerel gün gece yarısı civarında
farklı.

## Metne çevirmek

```python
df["date"].dt.strftime("%Y-%m")        # '2024-03'
df["date"].dt.strftime("%d.%m.%Y")     # '09.03.2024'
```

Sonuç metin. Gruplama için çoğu zaman `dt.to_period("M")` daha iyi: sıralı
kalıyor ve tarih olarak davranmaya devam ediyor.
