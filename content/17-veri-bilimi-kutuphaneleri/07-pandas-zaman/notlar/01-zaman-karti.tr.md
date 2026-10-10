## Okumak ve parçalamak

| Yazım | Ne yapar |
|---|---|
| `pd.to_datetime(s, format="%d.%m.%Y")` | metni tarihe çevirir |
| `errors="coerce"` | okunamayanı `NaT` yapar |
| `s.dt.year` / `.month` / `.day` / `.hour` | parçalar |
| `s.dt.dayofweek` | Pazartesi = 0 … Pazar = 6 |
| `s.dt.day_name()` | gün adı |
| `s.dt.strftime("%d/%m")` | biçimli metin |
| `s.dt.to_period("M")` | ay dönemi |
| `s.dt.tz_localize("UTC")` / `.dt.tz_convert(...)` | sütunda saat dilimi |

## Tarih indeksi

| Yazım | Ne yapar |
|---|---|
| `pd.date_range(baş, periods=n, freq="D")` | düzenli tarihler |
| `s.loc["2026-02"]` | şubatın hepsi |
| `s.loc["2026-03-10":"2026-03-12"]` | aralık (iki uç dahil) |
| `s.resample("ME").sum()` | aylık toplam |
| `s.asfreq("D")` | eksik günleri `NaN` ile ekler |
| `s.shift(1)` / `diff()` / `pct_change()` | önceki değerle karşılaştırma |
| `s.rolling(7).mean()` | son 7 satır |
| `s.rolling("7D").mean()` | son 7 gün |

## Sıklık kodları

| Kod | Anlam |
|---|---|
| `"D"` / `"h"` / `"min"` | gün / saat / dakika |
| `"W"` | pazar günü biten hafta |
| `"W-MON"` | pazartesi günleri |
| `"ME"` / `"MS"` | ay sonu / ay başı |
| `"QE"` / `"YE"` | çeyrek sonu / yıl sonu |

## Hatalar

| Belirti | Sebep |
|---|---|
| `doesn't match format` | sütunda karışık biçim |
| `'M' is no longer supported` | pandas 3'te `"ME"` |
| `Cannot compare tz-naive and tz-aware` | dilimli ile dilimsiz karıştı |
| `resample`'da `Only valid with DatetimeIndex` | indeks hâlâ metin; `to_datetime` |
| İlk hafta ortalaması tuhaf | ilk kova kısa |
| Kayan ortalama eksik günü görmüyor | `rolling(n)` satır sayar |
