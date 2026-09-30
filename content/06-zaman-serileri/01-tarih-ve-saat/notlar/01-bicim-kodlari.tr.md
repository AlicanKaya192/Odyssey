`strptime` (metni oku) ve `strftime` (metne yaz) aynı kodları kullanıyor.
Örnekler `datetime(2024, 3, 9, 14, 5, 7)` için.

## Tarih kodları

| Kod | Anlamı | Örnek |
|---|---|---|
| `%Y` | Dört haneli yıl | `2024` |
| `%y` | İki haneli yıl | `24` |
| `%m` | Ay, iki hane | `03` |
| `%d` | Gün, iki hane | `09` |
| `%j` | Yılın kaçıncı günü | `069` |
| `%B` | Ayın adı | `March` |
| `%b` | Ayın kısa adı | `Mar` |
| `%A` | Günün adı | `Saturday` |
| `%a` | Günün kısa adı | `Sat` |
| `%w` | Haftanın günü, pazar 0 | `6` |

## Saat kodları

| Kod | Anlamı | Örnek |
|---|---|---|
| `%H` | Saat, 00–23 | `14` |
| `%I` | Saat, 01–12 | `02` |
| `%p` | AM / PM | `PM` |
| `%M` | Dakika | `05` |
| `%S` | Saniye | `07` |
| `%f` | Mikrosaniye | `000000` |
| `%z` | UTC farkı | `+0300` |
| `%Z` | Dilim adı | `UTC` |

**Büyük-küçük harf farklı anlam taşıyor:** `%m` ay, `%M` dakika. `%y` iki
haneli yıl, `%Y` dört haneli.

## Sık karşılaşılan biçimler

| Metin | Biçim |
|---|---|
| `2024-03-09` | `fromisoformat` ya da `%Y-%m-%d` |
| `2024-03-09 14:05:07` | `fromisoformat` ya da `%Y-%m-%d %H:%M:%S` |
| `2024-03-09T14:05:07+03:00` | `fromisoformat` |
| `09.03.2024` | `%d.%m.%Y` |
| `09/03/2024` (Avrupa) | `%d/%m/%Y` |
| `03/09/2024` (ABD) | `%m/%d/%Y` |
| `9 March 2024` | `%d %B %Y` |
| `Mar 9, 2024` | `%b %d, %Y` |
| `20240309` | `%Y%m%d` |

## Çevirme yolları

```python
from datetime import date, datetime, timedelta, timezone

datetime.strptime("09.03.2024", "%d.%m.%Y")   # metin -> datetime
datetime.fromisoformat("2024-03-09 14:05")      # ISO metin -> datetime
date.fromisoformat("2024-03-09")                # ISO metin -> date

dt = datetime(2024, 3, 9, 14, 5)
dt.strftime("%d.%m.%Y %H:%M")                   # datetime -> metin
dt.isoformat()                                  # '2024-03-09T14:05:00'
dt.date()                                       # datetime -> date
datetime.combine(date(2024, 3, 9), dt.time())   # date + time -> datetime

datetime.fromtimestamp(1710000000, tz=timezone.utc)   # Unix saniye -> datetime
dt.replace(tzinfo=timezone.utc).timestamp()           # datetime -> Unix saniye
```

## `timedelta` başvurusu

```python
timedelta(weeks=1, days=2, hours=3, minutes=30, seconds=15)

gap = datetime(2024, 3, 10, 6, 5) - datetime(2024, 3, 9, 22, 15)
gap.days              # 0      tam gun sayisi
gap.seconds           # 28200  gunden artan saniye (0..86399)
gap.total_seconds()   # 28200.0  toplam saniye
gap / timedelta(hours=1)   # 7.833...  saat cinsinden
```

**`.seconds` toplam saniye değil.** 1 gün 2 saatlik bir sürede `.seconds`
yalnızca 7200 veriyor (günleri saymıyor). Toplam için `total_seconds()`.

Takvim bilgisi gerektiren adımlar (`timedelta` yapamaz):

| İstenen | Neden olmaz | Nerede |
|---|---|---|
| Bir ay sonra | Ay uzunluğu değişken | `pd.DateOffset(months=1)`, Bölüm 04 |
| Bir yıl sonra | Artık yıl | `pd.DateOffset(years=1)` |
| Ayın son günü | Ayın uzunluğu | `pd.offsets.MonthEnd()` |
| Sonraki iş günü | Hafta sonu, tatil | `pd.offsets.BDay()` |
