`date_range`, `asfreq`, `resample`, `floor` ve `round` aynı kısaltmaları
kullanıyor.

## Sabit uzunluktaki birimler

| Kısaltma | Anlamı | Örnek |
|---|---|---|
| `s` | Saniye | `30s` |
| `min` | Dakika | `15min` |
| `h` | Saat | `6h` |
| `D` | Takvim günü | `7D` |
| `W` | Hafta (pazar biten) | `W` |
| `W-MON` | Pazartesi biten hafta | `W-MON` |
| `B` | İş günü (pazartesi–cuma) | `B` |

Başına sayı yazılabiliyor: `15min`, `6h`, `2D`, `2W`.

## Takvime bağlı birimler

| Kısaltma | Anlamı | 2024'te ilk değer |
|---|---|---|
| `ME` | Ay sonu | 31 Ocak |
| `MS` | Ay başı | 1 Ocak |
| `BME` | Ayın son iş günü | 31 Ocak |
| `QE` | Çeyrek sonu | 31 Mart |
| `QS` | Çeyrek başı | 1 Ocak |
| `YE` | Yıl sonu | 31 Aralık |
| `YS` | Yıl başı | 1 Ocak |

`E` "end" (son), `S` "start" (baş). Ay ve çeyrek sabit uzunlukta olmadığı için
`floor("ME")` yazılamıyor; bunlar yalnızca `date_range`, `asfreq` ve
`resample` içinde çalışıyor.

## Eski adlar artık çalışmıyor

Eski derslerde ve cevaplarda şunları görürsün; yeni pandas hata veriyor:

| Eski | Yeni |
|---|---|
| `M` | `ME` |
| `Q` | `QE` |
| `Y`, `A` | `YE` |
| `H` | `h` |
| `T` | `min` |
| `S` | `s` |
| `BM` | `BME` |

Hata mesajı: `Invalid frequency: M`. `MS`, `QS`, `YS`, `D`, `W` ve `B`
değişmedi.

## `date_range` kalıpları

Üç bilgiden ikisi: başlangıç, bitiş, adet (`periods`).

```python
pd.date_range("2024-01-01", "2024-12-31", freq="D")     # yilin butun gunleri: 366
pd.date_range("2024-01-01", periods=12, freq="MS")      # 12 ay basi
pd.date_range(end="2024-12-31", periods=7, freq="D")    # son 7 gun
pd.date_range("2024-03-09", periods=24, freq="h")       # bir gunun saatleri
pd.date_range("2024-03-04", "2024-03-29", freq="B")     # is gunleri
pd.date_range("2024-01-01", periods=5, freq="W-MON")    # 5 pazartesi
pd.date_range("2024-03-09 09:00", "2024-03-09 17:00", freq="30min")
pd.date_range("2024-03-09", periods=3, freq="D", tz="Europe/Istanbul")   # dilimli
```

Başlangıç frekansa uymuyorsa pandas ilk uygun noktaya atlıyor:
`pd.date_range("2024-01-15", periods=2, freq="ME")` → 31 Ocak, 29 Şubat.

## Kaç adım var?

| Veri | Bir günde | Bir haftada | Bir yılda |
|---|---|---|---|
| Saatlik (`h`) | 24 | 168 | 8760 (artık yılda 8784) |
| Günlük (`D`) | 1 | 7 | 365 (artık yılda 366) |
| İş günü (`B`) | 1 | 5 | yaklaşık 261 |
| Haftalık (`W`) | — | 1 | yaklaşık 52 |
| Aylık (`ME`) | — | — | 12 |

Bu sayılar ileride **mevsim uzunluğu** olarak geri gelecek: saatlik veride
günlük desen 24, haftalık desen 168 adım; günlük veride haftalık desen 7,
yıllık desen 365; aylık veride yıllık desen 12.
