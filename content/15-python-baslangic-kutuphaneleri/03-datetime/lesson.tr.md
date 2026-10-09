# datetime

Bir siparişin kaç gün önce verildiği, bir aboneliğin ne zaman biteceği, bir
toplantının New York'ta saat kaçta olduğu, bir dosyadaki `05/03/2026` metninin
hangi gün olduğu... Tarih ve saatle ilgili her iş **`datetime`** modülüyle
yapılır. Bu bölümde tarih nesnelerini kurmayı, aralarındaki farkı (süre)
hesaplamayı, metne çevirip metinden okumayı ve saat dilimlerini görüyoruz.

## Üç nesne: date, time, datetime

```python
from datetime import date, time, datetime

d = date(2026, 3, 15)
t = time(14, 30)
dt = datetime(2026, 3, 15, 14, 30)
print(d, t, dt)
print(dt.year, dt.month, dt.day, dt.hour, dt.minute)
print(d.weekday(), d.isoweekday(), d.strftime("%A"))
print(datetime.combine(d, t) == dt, dt.date() == d)
```

```text
2026-03-15 14:30:00 2026-03-15 14:30:00
2026 3 15 14 30
6 7 Sunday
True True
```

- **`date`** yalnızca gün (yıl, ay, gün), **`time`** yalnızca saat,
  **`datetime`** ikisi birden.
- Parçalar özellik olarak okunur: `dt.year`, `dt.hour`...
- `weekday()` Pazartesi'yi 0 sayar, `isoweekday()` 1. 15 Mart 2026 bir Pazar:
  6 ve 7.
- `datetime.combine(gün, saat)` ikisini birleştirir, `dt.date()` günü ayırır.

Bugünün tarihi `date.today()`, şu anki an `datetime.now()` ile alınır. Her
çalıştırmada başka sonuç verdikleri için bu bölümdeki örneklerde sabit
tarihler kullanıyoruz; alıştırmalarda da tarih hep parametre olarak gelir.

## Süre: timedelta

İki tarihin farkı bir **`timedelta`** (süre) nesnesidir; tarihe süre eklenip
çıkarılabilir.

```python
from datetime import date, datetime, timedelta

start = date(2026, 3, 15)
print(start + timedelta(days=30))
print(date(2026, 12, 31) - start)
gap = datetime(2026, 3, 16, 9, 0) - datetime(2026, 3, 15, 14, 30)
print(gap, gap.days, gap.seconds, gap.total_seconds())
print(timedelta(weeks=2, hours=36))
print(date(2026, 3, 15) < date(2026, 4, 1))
```

```text
2026-04-14
291 days, 0:00:00
18:30:00 0 66600 66600.0
15 days, 12:00:00
True
```

15 Mart'tan 30 gün sonrası 14 Nisan; yıl sonuna 291 gün var. Dün 14:30 ile
bugün 09:00 arası 18,5 saat: `gap.days` 0, `gap.seconds` 66 600. Dikkat:
`seconds` gün kısmını **içermez**; toplam süre gerekiyorsa her zaman
**`total_seconds()`**. Tarihler `<`, `>`, `==` ile karşılaştırılır, `sorted`
ile sıralanır.

`timedelta`'nın `days`, `weeks`, `hours`, `minutes`, `seconds` parametreleri
var ama **`months` ve `years` yok**: ayların uzunluğu farklı olduğu için
"bir ay sonra" sabit bir süre değil. Ay eklemek ikinci notta.

## Metne çevirmek ve metinden okumak

```python
from datetime import datetime

dt = datetime(2026, 3, 5, 9, 7)
print(dt.strftime("%d.%m.%Y %H:%M"))
print(dt.strftime("%Y-%m-%d"), dt.isoformat())
parsed = datetime.strptime("05/03/2026 09:07", "%d/%m/%Y %H:%M")
print(parsed == dt)
print(datetime.fromisoformat("2026-03-05T09:07:00"))
```

```text
05.03.2026 09:07
2026-03-05 2026-03-05T09:07:00
True
2026-03-05 09:07:00
```

- **`strftime`** (string **f**ormat **time**): tarih → metin.
- **`strptime`** (string **p**arse **time**): metin → tarih; biçim metnin
  kendisiyle birebir eşleşmeli.
- **`isoformat` / `fromisoformat`**: uluslararası `YYYY-MM-DD` biçimi. Veri
  saklarken ve dosya adında bunu kullan: metin olarak sıralanınca da tarih
  sırasına girer.

En çok kullanılan biçim kodları:

| Kod | Anlamı | Örnek |
|---|---|---|
| `%Y` | dört haneli yıl | 2026 |
| `%m` | ay (01–12) | 03 |
| `%d` | gün (01–31) | 05 |
| `%H` | saat (00–23) | 09 |
| `%M` | dakika (00–59) | 07 |
| `%S` | saniye | 00 |
| `%A` / `%a` | gün adı / kısa | Thursday / Thu |
| `%B` / `%b` | ay adı / kısa | March / Mar |

Küçük `%m` **ay**, büyük `%M` **dakika**; karıştırmak en sık hatadır. Gün ve
ay adları sistemin dil ayarına göre değişebilir; programın her yerde aynı
çalışması gerekiyorsa adları kendi listenden al (`["Mon", "Tue", ...][d.weekday()]`).

## Saat dilimleri

Şimdiye kadarki `datetime` nesneleri **saf** (naive): hangi saat diliminde
olduklarını bilmiyorlar. `tzinfo` verilen nesne **farkında** (aware) olur.
Saat dilimleri `zoneinfo` modülüyle, `"Bölge/Şehir"` adıyla alınır.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

meeting = datetime(2026, 3, 15, 14, 30, tzinfo=ZoneInfo("Europe/Istanbul"))
print(meeting)
print(meeting.astimezone(ZoneInfo("America/New_York")))
print(meeting.astimezone(timezone.utc))
summer = datetime(2026, 7, 15, 12, 0, tzinfo=ZoneInfo("Europe/London"))
winter = datetime(2026, 1, 15, 12, 0, tzinfo=ZoneInfo("Europe/London"))
print(summer.utcoffset(), winter.utcoffset())
```

```text
2026-03-15 14:30:00+03:00
2026-03-15 07:30:00-04:00
2026-03-15 11:30:00+00:00
1:00:00 0:00:00
```

İstanbul'da 14:30 olan toplantı New York'ta 07:30, UTC'de 11:30.
**`astimezone`** aynı anı başka bir saatte gösterir. Londra yazın UTC+1,
kışın UTC+0: **yaz saati** uygulaması yüzünden fark yılın içinde değişiyor.
Bu yüzden saat farkını elle (`+ timedelta(hours=3)`) yazmak yanlıştır;
`ZoneInfo` hangi tarihte hangi farkın geçerli olduğunu biliyor.

Sunucularda ve veritabanlarında zamanı **UTC** olarak saklamak, kullanıcıya
gösterirken onun saat dilimine çevirmek yaygın bir kuraldır.

## Sık hatalar

```python
from datetime import date, datetime
from zoneinfo import ZoneInfo

naive = datetime(2026, 3, 15, 14, 30)
aware = datetime(2026, 3, 15, 14, 30, tzinfo=ZoneInfo("Europe/Istanbul"))
try:
    print(aware - naive)
except TypeError as error:
    print("TypeError:", error)
try:
    datetime.strptime("2026-13-01", "%Y-%m-%d")
except ValueError as error:
    print("ValueError:", error)
try:
    date(2026, 1, 31).replace(month=2)
except ValueError as error:
    print("ValueError:", error)
print(datetime.strptime("09:07", "%H:%m"))
```

```text
TypeError: can't subtract offset-naive and offset-aware datetimes
ValueError: time data '2026-13-01' does not match format '%Y-%m-%d'
ValueError: day 31 must be in range 1..28 for month 2 in year 2026
1900-07-01 09:00:00
```

- Saf ve farkında nesneler birbirinden çıkarılamaz, karşılaştırılamaz.
- 13. ay yok: `strptime` biçime uymayan metinde `ValueError` verir. Dosyadan
  okunan tarihleri `try` ile okumak gerekir.
- 31 Ocak'ın ayını 2 yapmak 31 Şubat ister; o gün yok.
- `"%H:%m"` yazılınca 07 **ay** olarak okundu: sonuç 1900 yılının Temmuz'u.
  Hata vermediği için en sinsi olanı bu.

## Özet

- `date` gün, `time` saat, `datetime` ikisi; parçalar `year`, `month`,
  `hour` gibi özelliklerle okunur.
- İki tarihin farkı `timedelta`; toplam süre `total_seconds()`. Ay ve yıl
  `timedelta`'da yok.
- `strftime` tarih → metin, `strptime` metin → tarih; `%m` ay, `%M` dakika.
- Saklamak için ISO biçimi (`isoformat`, `fromisoformat`).
- Saat dilimi `ZoneInfo("Europe/Istanbul")`; çevirmek `astimezone`. Farkı elle
  yazma, yaz saati değiştirir.
