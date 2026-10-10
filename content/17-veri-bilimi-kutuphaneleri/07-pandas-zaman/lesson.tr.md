# pandas ile Zaman

Tarih, veride en sık rastlanan ve en çok sorun çıkaran türdür: dosyada metin
olarak gelir, her ülke başka biçimde yazar, aylar farklı uzunluktadır, saat
dilimleri yaz saatiyle kayar. pandas bunların hepsi için bir araç sunuyor:
`to_datetime`, `.dt` erişimcisi, tarih indeksi, `resample`, `shift` /
`rolling` ve saat dilimleri. Bu bölüm bu araçları anlatıyor; tahmin
modelleri **Zaman Serileri** patikasının konusu.

## Metni tarihe çevirmek

```python
import pandas as pd

raw = pd.Series(["2026-03-02", "2026-03-15", "15.03.2026", "unknown"])
try:
    pd.to_datetime(raw)
except ValueError as error:
    print("ValueError:", str(error).split(". ")[0])
dates = pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
print(dates.tolist())
print(dates.isna().sum())
tr = pd.to_datetime("15.03.2026", format="%d.%m.%Y")
print(tr.date(), tr.day_name())
```

```text
ValueError: time data "15.03.2026" doesn't match format "%Y-%m-%d"
[Timestamp('2026-03-02 00:00:00'), Timestamp('2026-03-15 00:00:00'), NaT, NaT]
2
2026-03-15 Sunday
```

- `to_datetime` biçimi **ilk elemandan** tahmin eder (`%Y-%m-%d`) ve sonra
  hepsine uygular; `15.03.2026` buna uymayınca hata verir. Karışık biçimli
  bir sütun sessizce yanlış okunmaz, durur.
- `format=` biçimi açıkça söyler; hem hızlıdır hem de 03/04'ün mart mı
  nisan mı olduğu tartışmasını bitirir.
- `errors="coerce"` okunamayanı `NaT` (Not a Time, tarihlerin `NaN`'ı) yapar.
  Ardından **kaç tane** olduğuna bakmak şart: burada 2 kayıt kayboldu.
- Türkiye'deki gün.ay.yıl yazımı için `format="%d.%m.%Y"`.

## .dt: tarihin parçaları

```python
import pandas as pd

s = pd.Series(pd.to_datetime(["2026-03-02 09:30", "2026-03-07 18:05",
                              "2026-04-01 00:00"]))
print(s.dt.year.tolist(), s.dt.month.tolist(), s.dt.dayofweek.tolist())
print(s.dt.day_name().tolist())
print(s.dt.strftime("%d/%m").tolist(), s.dt.hour.tolist())
print((s.dt.dayofweek >= 5).tolist())
print(s.dt.to_period("M").astype(str).tolist())
```

```text
[2026, 2026, 2026] [3, 3, 4] [0, 5, 2]
['Monday', 'Saturday', 'Wednesday']
['02/03', '07/03', '01/04'] [9, 18, 0]
[False, True, False]
['2026-03', '2026-03', '2026-04']
```

- Tarih sütununda metodlar `.dt` üzerinden gelir (metindeki `.str` gibi):
  `year`, `month`, `day`, `hour`, `dayofweek`, `day_name()`.
- `dayofweek` **Pazartesi = 0**, Pazar = 6. Hafta sonu: `>= 5`.
- `strftime` istediğin biçimde metin üretir; rapor ve grafik etiketleri için.
- `to_period("M")` tarihi bir **ay** dönemine çevirir: "2026-03". Ay bazında
  gruplamak için gün bilgisini atmanın temiz yolu.

## Tarih indeksi ve dilim

```python
import pandas as pd

days = pd.date_range("2026-01-01", periods=90, freq="D")
sales = pd.Series(range(90), index=days)
print(sales.index[:2].tolist())
print(len(sales.loc["2026-02"]), sales.loc["2026-02"].iloc[0])
print(sales.loc["2026-03-10":"2026-03-12"].tolist())
ends = pd.date_range("2026-01-31", periods=3, freq="ME")
mondays = pd.date_range("2026-03-02", periods=3, freq="W-MON")
print(ends.strftime("%Y-%m-%d").tolist())
print(mondays.strftime("%Y-%m-%d").tolist())
```

```text
[Timestamp('2026-01-01 00:00:00'), Timestamp('2026-01-02 00:00:00')]
28 31
[68, 69, 70]
['2026-01-31', '2026-02-28', '2026-03-31']
['2026-03-02', '2026-03-09', '2026-03-16']
```

- `date_range` düzenli aralıklı tarihler üretir: `freq="D"` gün, `"W-MON"`
  her pazartesi, `"ME"` ay sonu (month end).
- İndeks tarih olunca dilim **metinle** yazılabilir: `loc["2026-02"]` şubatın
  bütün günleri (28 gün, ilk değer 31), `loc["2026-03-10":"2026-03-12"]`
  iki ucu dahil.
- `"ME"` ayların farklı uzunluğunu bilir: 31 ocak, 28 şubat, 31 mart.

## resample: zamana göre gruplamak

```python
import pandas as pd

days = pd.date_range("2026-01-01", periods=90, freq="D")
sales = pd.Series(range(90), index=days)
monthly = sales.resample("ME").sum()
print(monthly.index.strftime("%Y-%m-%d").tolist(), monthly.tolist())
weekly = sales.resample("W").mean()
print(len(weekly), weekly.iloc[0], weekly.index[0].date())
try:
    sales.resample("M").sum()
except ValueError as error:
    print("ValueError:", str(error).split('("')[1].rstrip('")'))
```

```text
['2026-01-31', '2026-02-28', '2026-03-31'] [465, 1246, 2294]
14 1.5 2026-01-04
ValueError: 'M' is no longer supported for offsets. Please use 'ME' instead.
```

- `resample` zaman için `groupby`'dır: günlük veriyi aylık, haftalık ya da
  saatlik kovalara toplar. Arkasından `sum`, `mean`, `max` gelir.
- Etiket kovanın **sonu**: ocak toplamı `2026-01-31` etiketli.
- `"W"` haftayı pazar günü bitirir. 1 Ocak 2026 perşembe; ilk hafta yalnızca
  4 günlük (1–4 Ocak), ortalaması 1,5. Kısa ilk ve son kovaya dikkat.
- Eski kodlarda gördüğün `"M"` pandas 3'te kalktı; ay sonu `"ME"`, çeyrek
  sonu `"QE"`, yıl sonu `"YE"`.

## shift, diff, pct_change ve rolling

```python
import pandas as pd

idx = pd.date_range("2026-01-01", periods=5, freq="D")
s = pd.Series([100, 110, 99, 120, 120], index=idx)
print(s.shift(1).tolist())
print(s.diff().tolist())
print(s.pct_change().round(3).tolist())
print(s.rolling(3).mean().round(1).tolist())
print(s.rolling("3D").mean().round(1).tolist())
```

```text
[nan, 100.0, 110.0, 99.0, 120.0]
[nan, 10.0, -11.0, 21.0, 0.0]
[nan, 0.1, -0.1, 0.212, 0.0]
[nan, nan, 103.0, 109.7, 113.0]
[100.0, 105.0, 103.0, 109.7, 113.0]
```

- `shift(1)` her değeri bir adım ileri kaydırır: "dünün değeri". İlk satırın
  dünü yok, `NaN`.
- `diff()` = bugün − dün, `pct_change()` = değişim oranı (110 / 100 − 1 =
  0,1).
- `rolling(3)` son 3 **satırın** ortalaması; ilk iki satırda 3 değer olmadığı
  için `NaN`.
- `rolling("3D")` son 3 **günün** ortalaması: elinde kaç gün varsa onunla
  başlar. Eksik günü olan veride ikisi ayrışır: satır sayısı ile gün sayısı
  artık aynı şey değildir.

## Saat dilimleri ve süreler

```python
import pandas as pd

t = pd.Timestamp("2026-03-29 01:30")
utc = t.tz_localize("UTC")
print(utc, utc.tz_convert("Europe/Istanbul"))
print(utc.tz_convert("Europe/Berlin"))
naive = pd.Timestamp("2026-03-29 12:00")
try:
    print(naive < utc)
except TypeError as error:
    print("TypeError:", error)
gap = pd.Timestamp("2026-03-31") - pd.Timestamp("2026-03-02 12:00")
print(gap, gap.days, gap.total_seconds() / 3600)
```

```text
2026-03-29 01:30:00+00:00 2026-03-29 04:30:00+03:00
2026-03-29 03:30:00+02:00
TypeError: Cannot compare tz-naive and tz-aware timestamps
28 days 12:00:00 28 684.0
```

- Saat dilimi olmayan tarih (naive) "hangi saatte?" sorusuna cevap vermez.
  `tz_localize("UTC")` ona dilim **yazar**, `tz_convert` aynı anı başka bir
  dilimde **gösterir**.
- Türkiye yıl boyu UTC+3. Berlin 29 Mart 2026 gecesi yaz saatine geçti; aynı
  an orada 03:30 (+02:00). Birden fazla ülkenin verisini birleştirirken
  her şeyi önce UTC'ye çevirmek bu kaymaları ortadan kaldırır.
- Dilimli ile dilimsiz tarih karşılaştırılamaz: `TypeError`.
- İki tarihin farkı `Timedelta`: `days` yalnızca tam günleri verir (28),
  tamamı için `total_seconds()`.

## Özet

- `to_datetime(..., format=..., errors="coerce")`; ardından `NaT` sayısına bak.
- `.dt` ile parçalar (`dayofweek` Pazartesi = 0), `to_period("M")` ile ay.
- Tarih indeksinde metinle dilim; `resample("ME")` zamana göre gruplar
  (`"M"` pandas 3'te yok).
- `shift` / `diff` / `pct_change` önceki değerle karşılaştırır; `rolling(n)`
  satır, `rolling("nD")` gün sayar.
- Saat dilimlerinde önce UTC; dilimli ve dilimsiz karıştırılmaz.
