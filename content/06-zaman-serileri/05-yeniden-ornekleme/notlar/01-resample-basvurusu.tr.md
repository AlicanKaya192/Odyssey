## Kalıp

```python
s.resample("<frekans>").<islem>()
```

Önce kovalar (`"W"`, `"ME"`, `"h"`, `"15min"`...), sonra kovanın içindekileri
tek sayıya indiren işlem.

## İşlemler

| İşlem | Verdiği | Boş kovada |
|---|---|---|
| `sum()` | Toplam | `0` |
| `sum(min_count=1)` | Toplam | `NaN` |
| `mean()` | Ortalama | `NaN` |
| `median()` | Ortanca | `NaN` |
| `max()`, `min()` | En büyük, en küçük | `NaN` |
| `first()`, `last()` | Kovanın ilk / son geçerli değeri | `NaN` |
| `count()` | Geçerli değer sayısı | `0` |
| `size()` | Satır sayısı (`NaN` dahil) | `0` |
| `std()` | Standart sapma | `NaN` |
| `ohlc()` | Açılış, en yüksek, en düşük, kapanış | `NaN` |
| `nunique()` | Farklı değer sayısı | `0` |
| `agg(["sum", "mean"])` | Birden çok özet, sütun sütun | — |
| `agg(fonksiyon)` | Kendi fonksiyonun | — |

Tabloda (DataFrame) sütun başına ayrı işlem:

```python
df.resample("W").agg({"sales": "sum", "price": "mean", "stock": "last"})
```

## Hangi değer, hangi işlem

| Değer türü | Örnek | Seyreltirken | Sıklaştırırken |
|---|---|---|---|
| Akış (birikir) | Satış, tüketim, ziyaret, yağış | `sum` | Paylaştır (böl) |
| Anlık seviye | Fiyat, stok, bakiye | `last` | `ffill` |
| Anlık ölçüm | Sıcaklık, hız, yük | `mean` (tepe için `max`) | `interpolate` |
| Oran | Dönüşüm oranı, doluluk | Ağırlıklı ortalama | `ffill` |
| Sayım | Olay, hata, sipariş adedi | `sum` ya da `count` | Paylaştır |

**Oranların ortalaması tuzaklı.** Günlük dönüşüm oranlarının düz ortalaması
haftalık oranı vermiyor; pay ile paydayı ayrı ayrı toplayıp sonra bölmek
gerekiyor:

```python
weekly = df.resample("W").agg({"orders": "sum", "visits": "sum"})
weekly["rate"] = weekly["orders"] / weekly["visits"]
```

## Etiket ve kapalı uç

| Frekans | Kova | Etiket |
|---|---|---|
| `"D"`, `"h"`, `"15min"` | Başlangıç dahil, bitiş hariç | Kovanın **başı** |
| `"W"` (= `"W-SUN"`) | Pazartesi–pazar | Kovanın **sonu** (pazar) |
| `"W-MON"` | Salı–pazartesi | Pazartesi |
| `"ME"`, `"QE"`, `"YE"` | Takvim ayı / çeyreği / yılı | Dönemin **son** günü |
| `"MS"`, `"QS"`, `"YS"` | Aynı kovalar | Dönemin **ilk** günü |

```python
# hafta pazar baslasin, etiket haftanin basi olsun
s.resample("W", label="left", closed="left").sum()

# "saat sonu" olcumleri icin
s.resample("h", label="right", closed="right").mean()

# gunu 06:00'da baslat
load.resample("24h", offset="6h").sum()
```

Bir sayaç değeri saatin **sonunda** yazıyorsa (14:00 satırı 13:00–14:00
arasını anlatıyorsa) varsayılan kovalama bir saat kayık oluyor; o zaman
`closed="right", label="right"`.

## Kovaları denetlemek

```python
counts = s.resample("W").count()
weekly = s.resample("W").sum()
full = weekly[counts == 7]                 # yalnizca tam haftalar

s.resample("W").sum(min_count=7)           # eksik kova NaN olsun
s.resample("ME").agg(["sum", "count"])     # ikisini yan yana gor
```

Beklenen gözlem sayısı: haftada 7 gün, günde 24 saat, ayda
`index.days_in_month`.

## `resample`, `asfreq`, `groupby`

| Araç | Ne yapıyor | Ne zaman |
|---|---|---|
| `s.resample("ME").sum()` | Kovalara ayırıp özetliyor | Frekansı değiştirmek |
| `s.asfreq("D")` | Satır açıyor, değer hesaplamıyor | Eksikleri görünür kılmak |
| `s.groupby(s.index.to_period("M")).sum()` | Döneme göre gruplayıp özetliyor | Periyot indeksi istenince |
| `s.groupby(s.index.month).mean()` | **Bütün yılların** aynı ayını birleştiriyor | Mevsim profili (Bölüm 09) |

Son satır çok karıştırılıyor: `resample("ME")` 36 ay veriyor (her yılın her
ayı ayrı), `groupby(index.month)` 12 satır veriyor (bütün Ocaklar birlikte).
