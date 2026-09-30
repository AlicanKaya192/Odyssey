# Python'da Tarih ve Saat

Bir önceki bölümde tarihler metindi: `"2022-01-01"`. Metinle sıralama
yapabildik, ilk dört karakterden yılı aldık. Ama şu soruların hiçbirine metin
cevap veremiyor:

- 27 Şubat ile 4 Mart arasında kaç gün var?
- 9 Mart 2024 haftanın hangi günü?
- Saat 22:15'te başlayan 7 saat 50 dakikalık vardiya ne zaman bitiyor?

Cevaplar takvime bağlı: ayların uzunluğu farklı, bazı yıllar 366 gün, gece
yarısını geçen bir süre ertesi güne taşıyor. Bunları bilen bir **tür**
gerekiyor. Python'da bu tür standart kütüphanedeki `datetime` modülünden
geliyor; pandas'taki tarihlerin hepsi de aynı fikrin üstüne kurulu. Bu bölümü
iyi öğrenirsen sonraki bölümlerin yarısını zaten bilmiş oluyorsun.

## Dört tür

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>date</code></span><span>Yalnızca gün: <code>date(2024, 3, 9)</code></span></div>
    <div class="anat-row"><span><code>time</code></span><span>Yalnızca saat: <code>time(14, 30)</code>; tek başına az kullanılıyor</span></div>
    <div class="anat-row"><span><code>datetime</code></span><span>Gün ve saat birlikte: <code>datetime(2024, 3, 9, 14, 30)</code></span></div>
    <div class="anat-row"><span><code>timedelta</code></span><span>Bir <b>an</b> değil, bir <b>süre</b>: <code>timedelta(days=6)</code></span></div>
  </div>
  <figcaption>İlk üçü takvimde bir noktayı, sonuncusu iki nokta arasındaki mesafeyi anlatıyor.</figcaption>
</figure>

```python
from datetime import date, datetime, time, timedelta

d = date(2024, 3, 9)
t = datetime(2024, 3, 9, 14, 30)

print(d)               # 2024-03-09
print(t)               # 2024-03-09 14:30:00
print(d.year, d.month, d.day)      # 2024 3 9
print(t.hour, t.minute)            # 14 30
```

Sıra her zaman büyükten küçüğe: **yıl, ay, gün, saat, dakika, saniye.**
`date(9, 3, 2024)` yazarsan Python 9. yılın 3. ayının 2024. gününü arıyor ve
hata veriyor.

**Geçersiz tarih kurulamıyor.** Bu, metne göre en büyük kazanç:

```python
date(2023, 2, 29)
# ValueError: day 29 must be in range 1..28 for month 2 in year 2023
```

2023 artık yıl değil; Şubat 28 gün. `"2023-02-29"` diye bir metin rahatça
yazılabiliyor ve fark edilmeden tabloda durabiliyor, `date` ise buna izin
vermiyor.

## Haftanın günü

```python
d = date(2024, 3, 9)
print(d.weekday())      # 5   (Pazartesi 0 ... Pazar 6)
print(d.isoweekday())   # 6   (Pazartesi 1 ... Pazar 7)
```

İki ayrı numaralama var ve ikisi de sık kullanılıyor. **`weekday()` sıfırdan
başlıyor**, `isoweekday()` birden. Hafta sonunu seçmek için
`d.weekday() >= 5` en kısa yol. pandas'ta da aynı kural geçerli: `dayofweek`
Pazartesi için 0.

## Süreler: `timedelta`

İki tarihin farkı bir **süre** veriyor; süre de ayrı bir tür.

```python
order = date(2024, 2, 27)
delivery = date(2024, 3, 4)

gap = delivery - order
print(gap)          # 6 days, 0:00:00
print(gap.days)     # 6
```

Aynı iki tarih 2023'te 5 gün ediyor: 2024'te araya 29 Şubat giriyor. Takvimi
elle hesaplasaydın bunu kaçırman çok kolaydı.

Süre elle de kurulabiliyor ve bir tarihe eklenebiliyor:

```python
start = datetime(2024, 3, 9, 22, 15)
end = start + timedelta(hours=7, minutes=50)

print(end)                             # 2024-03-10 06:05:00
print((end - start).total_seconds())   # 28200.0
```

Gece yarısını geçti, tarih kendiliğinden ertesi güne döndü.

<figure class="fig">
  <div class="flow">
    <span class="node"><code>datetime</code></span><span class="arrow">−</span>
    <span class="node"><code>datetime</code></span><span class="arrow">=</span>
    <span class="node acc"><code>timedelta</code></span>
  </div>
  <div class="flow">
    <span class="node"><code>datetime</code></span><span class="arrow">+</span>
    <span class="node acc"><code>timedelta</code></span><span class="arrow">=</span>
    <span class="node"><code>datetime</code></span>
  </div>
  <figcaption>İki anın farkı bir süre, bir ana eklenen süre yeni bir an. İki anı toplamak ise anlamsız: <code>datetime + datetime</code> hata veriyor.</figcaption>
</figure>

**`timedelta` ay ve yıl bilmiyor.** `timedelta(months=1)` diye bir şey yok,
çünkü "bir ay" sabit bir süre değil: Ocak'ta 31 gün, Şubat'ta 28 ya da 29.
Günle yaklaşınca da yanlış çıkıyor:

```python
date(2024, 1, 31) + timedelta(days=30)    # 2024-03-01  ("bir ay sonra" degil)
date(2024, 2, 29) + timedelta(days=365)   # 2025-02-28  ("bir yil sonra" degil)
```

Takvime göre "bir ay sonra" pandas'ın `DateOffset`'iyle yapılıyor; Bölüm
04'te.

## Karşılaştırmak ve sıralamak

Tarihler sayılar gibi karşılaştırılıyor; `min`, `max` ve `sorted` doğru
çalışıyor:

```python
days = [date(2024, 3, 9), date(2023, 1, 10), date(2024, 12, 1)]
print(sorted(days))    # [2023-01-10, 2024-03-09, 2024-12-01]
print(max(days))       # 2024-12-01
```

Aynı üç tarih gün önde yazılmış metin olsaydı:

```python
sorted(["09.03.2024", "10.01.2023", "01.12.2024"])
# ['01.12.2024', '09.03.2024', '10.01.2023']   yanlis
```

Metin soldan sağa karşılaştırılıyor ve yalnızca günlere bakılmış oluyor.
Çözüm metni tarihe çevirmek.

## Metinden tarihe: `strptime`

Dosyadan, kullanıcıdan, bir sistemden gelen tarih hemen her zaman metin.
Çevirmek için **biçimi** söylemen gerekiyor:

```python
datetime.strptime("09.03.2024", "%d.%m.%Y")          # 2024-03-09 00:00:00
datetime.strptime("03/09/2024", "%m/%d/%Y")          # 2024-03-09 00:00:00
datetime.strptime("9 March 2024 14:30", "%d %B %Y %H:%M")
```

`%d` gün, `%m` ay, `%Y` dört haneli yıl. Biçimin geri kalanı (nokta, eğik
çizgi, boşluk) metinde birebir aynı olmalı.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>%d</code> → <code>09</code></span><span>Gün, iki hane</span></div>
    <div class="anat-row"><span><code>%m</code> → <code>03</code></span><span>Ay, iki hane (küçük m)</span></div>
    <div class="anat-row"><span><code>%Y</code> → <code>2024</code></span><span>Dört haneli yıl (büyük Y; <code>%y</code> iki hane)</span></div>
    <div class="anat-row"><span><code>%H</code> → <code>14</code></span><span>Saat, 00–23</span></div>
    <div class="anat-row"><span><code>%M</code> → <code>30</code></span><span>Dakika (büyük M)</span></div>
  </div>
  <figcaption><code>"09.03.2024 14:30"</code> metninin biçimi <code>"%d.%m.%Y %H:%M"</code>. Kodların tam listesi "Biçim Kodları" notunda.</figcaption>
</figure>

**`03/09/2024` tek başına belirsiz.** Amerika'da 9 Mart, Avrupa'da 3 Eylül.
Metne bakarak hangisi olduğunu anlamanın yolu yok; veriyi kimin ürettiğini
bilmen gerekiyor. `%d/%m` ile `%m/%d` karıştırılırsa ayın 12'sinden küçük
günlerde **hata bile vermiyor**, sessizce yanlış tarih üretiyor. Günü 12'den
büyük bir satır (`13/09/2024`) ararsan hangi biçim olduğunu anlarsın.

ISO 8601 metni için biçim yazmaya gerek yok:

```python
datetime.fromisoformat("2024-03-09 14:30")
date.fromisoformat("2024-03-09")
```

## Tarihten metne: `strftime`

Ters yön aynı kodlarla:

```python
d = date(2024, 3, 9)
print(d.strftime("%d.%m.%Y"))       # 09.03.2024
print(d.strftime("%A, %d %B"))      # Saturday, 09 March
print(d.isoformat())                # 2024-03-09
```

İki ismi karıştırmamak için: **`strptime` = parse** (metni oku),
**`strftime` = format** (metne yaz).

`%A` ve `%B` gün ve ay adlarını İngilizce veriyor. Bu isimler bilgisayarın
bölge ayarına göre değişebiliyor; bir sisteme kaydedeceğin tarihi hiçbir
zaman adla yazma, `isoformat()` kullan.

## ISO hafta numarası

"Yılın kaçıncı haftası?" sorusunun standart cevabı ISO haftası: hafta
pazartesi başlıyor ve yılın **ilk perşembesini içeren** hafta 1. hafta
sayılıyor.

```python
for d in [date(2024, 12, 29), date(2024, 12, 30), date(2025, 1, 1)]:
    print(d, d.isocalendar())
```

```text
2024-12-29 (year=2024, week=52, weekday=7)
2024-12-30 (year=2025, week=1, weekday=1)
2025-01-01 (year=2025, week=1, weekday=3)
```

**30 Aralık 2024, 2025'in 1. haftası.** Tersi de oluyor: 1 Ocak 2021, 2020'nin
53. haftası. Haftalık rapor yaparken yılı `d.year`'dan, haftayı
`isocalendar()`'dan alırsan yıl sonunda "2024'ün 1. haftası" gibi var olmayan
bir hafta üretiyorsun. **Hafta numarasıyla birlikte yılı da
`isocalendar()`'dan al.**

## Saat dilimleri

Buraya kadarki bütün `datetime` nesneleri **saat dilimsiz** (naive):
`14:30` yazıyor ama nerenin 14:30'u olduğunu bilmiyor. Tek bir şehirde
çalışırken sorun yok. Veri farklı yerlerden geliyorsa ya da yaz saati
uygulanan bir yerdeyse, dilimi olan (aware) zaman gerekiyor.

```python
from datetime import timezone
from zoneinfo import ZoneInfo

berlin = ZoneInfo("Europe/Berlin")
meeting = datetime(2024, 3, 31, 9, 0, tzinfo=berlin)

print(meeting.astimezone(timezone.utc))                    # 2024-03-31 07:00:00+00:00
print(meeting.astimezone(ZoneInfo("Europe/Istanbul")))     # 2024-03-31 10:00:00+03:00
```

`ZoneInfo` bölge adını (`"Europe/Berlin"`, `"America/New_York"`) alıyor ve o
bölgenin yaz saati kurallarını biliyor. **UTC** ise hiçbir yerin yerel saati
değil; yaz saati yok, kaymıyor. Bu yüzden ortak dil o.

**Yaz saati tuzağı.** Berlin 31 Mart 2024 gecesi saatleri bir saat ileri
aldı. Bir gün önceki toplantı aynı saatte ama İstanbul'da başka bir saate
denk geliyor:

```text
2024-03-30 09:00 Berlin  ->  11:00 Istanbul   (Berlin UTC+1)
2024-03-31 09:00 Berlin  ->  10:00 Istanbul   (Berlin UTC+2)
```

İstanbul 2016'dan beri yaz saati uygulamıyor, hep UTC+3. Fark her yıl iki kez
değişiyor.

Daha sinsi olanı süre hesabı:

```python
a = datetime(2024, 3, 30, 12, 0, tzinfo=berlin)
b = datetime(2024, 3, 31, 12, 0, tzinfo=berlin)

print(b - a)                                                 # 1 day, 0:00:00
print(b.astimezone(timezone.utc) - a.astimezone(timezone.utc))   # 23:00:00
```

Aynı dilimdeki iki zamanı çıkarınca Python **duvar saatine** bakıyor: 12:00'den
12:00'e "1 gün". Oysa gerçekte **23 saat** geçti; o gece bir saat hiç
yaşanmadı. Saatlik tüketim toplarken, bir makinenin çalışma süresini
hesaplarken bu fark doğrudan hatalı sonuç demek.

<figure class="fig">
  <svg viewBox="0 0 680 170" width="680" xmlns="http://www.w3.org/2000/svg"><text class="ink" x="16" y="52" font-size="12.5" font-weight="600">UTC</text><text class="ink" x="16" y="122" font-size="12.5" font-weight="600">Berlin</text><line class="line" x1="100" y1="48" x2="590" y2="48"/><line class="line" x1="100" y1="118" x2="590" y2="118"/><circle class="dot" cx="120" cy="48" r="4"/><text class="dim" x="120" y="34" font-size="11" text-anchor="middle">23:00</text><line class="curve3" stroke-dasharray="3 3" x1="120" y1="54" x2="120" y2="112"/><circle class="dot" cx="120" cy="118" r="4"/><text class="dim" x="120" y="140" font-size="11" text-anchor="middle">00:00</text><circle class="dot" cx="210" cy="48" r="4"/><text class="dim" x="210" y="34" font-size="11" text-anchor="middle">00:00</text><line class="curve3" stroke-dasharray="3 3" x1="210" y1="54" x2="210" y2="112"/><circle class="dot" cx="210" cy="118" r="4"/><text class="dim" x="210" y="140" font-size="11" text-anchor="middle">01:00</text><circle class="dot" cx="300" cy="48" r="4"/><text class="dim" x="300" y="34" font-size="11" text-anchor="middle">01:00</text><line class="curve3" stroke-dasharray="3 3" x1="300" y1="54" x2="300" y2="112"/><circle class="dot2" cx="300" cy="118" r="4"/><text class="dim" x="300" y="140" font-size="11" text-anchor="middle">03:00</text><circle class="dot" cx="390" cy="48" r="4"/><text class="dim" x="390" y="34" font-size="11" text-anchor="middle">02:00</text><line class="curve3" stroke-dasharray="3 3" x1="390" y1="54" x2="390" y2="112"/><circle class="dot" cx="390" cy="118" r="4"/><text class="dim" x="390" y="140" font-size="11" text-anchor="middle">04:00</text><circle class="dot" cx="480" cy="48" r="4"/><text class="dim" x="480" y="34" font-size="11" text-anchor="middle">03:00</text><line class="curve3" stroke-dasharray="3 3" x1="480" y1="54" x2="480" y2="112"/><circle class="dot" cx="480" cy="118" r="4"/><text class="dim" x="480" y="140" font-size="11" text-anchor="middle">05:00</text><circle class="dot" cx="570" cy="48" r="4"/><text class="dim" x="570" y="34" font-size="11" text-anchor="middle">04:00</text><line class="curve3" stroke-dasharray="3 3" x1="570" y1="54" x2="570" y2="112"/><circle class="dot" cx="570" cy="118" r="4"/><text class="dim" x="570" y="140" font-size="11" text-anchor="middle">06:00</text><text class="ink" x="255.0" y="160" font-size="11" text-anchor="middle">02:00–03:00 yok</text><text class="dim" x="664" y="16" font-size="11" text-anchor="end">30→31 Mart 2024</text></svg>
  <figcaption>UTC saatleri düzgün ilerliyor. Berlin'in duvar saati 01:00'den 03:00'e atlıyor: o gece bir saat hiç yaşanmadı. Aynı dilimde 12:00'den ertesi gün 12:00'e "1 gün" görünüyor ama arada 23 saat var.</figcaption>
</figure>

Kural basit ve sektörün standart uygulaması: **zamanı UTC olarak sakla ve
hesapla; yerel saate yalnızca insana gösterirken çevir.**

Sonbaharda tersi oluyor: 27 Ekim 2024 gecesi Berlin'de 02:00–03:00 arası iki
kez yaşandı. `02:30` yazan bir kayıt iki farklı ana karşılık geliyor. Python
ikisini `fold=0` (ilki) ve `fold=1` (ikincisi) ile ayırıyor; pandas'ta bunun
karşılığını Bölüm 02'de göreceğiz.

## Unix zamanı

Birçok sistem zamanı tek bir sayı olarak veriyor: **1 Ocak 1970 00:00 UTC'den
bu yana geçen saniye.** API'lerde, log dosyalarında, veritabanlarında çok sık.

```python
datetime.fromtimestamp(1710000000, tz=timezone.utc)
# 2024-03-09 16:00:00+00:00

datetime(2024, 3, 9, 16, 0, tzinfo=timezone.utc).timestamp()
# 1710000000.0
```

İki dikkat noktası:

- **`tz=timezone.utc` yazmayı unutma.** Yazmazsan Python sayıyı bilgisayarın
  yerel saatine çeviriyor ve aynı kod başka bir makinede başka sonuç veriyor.
- **13 haneli sayılar milisaniye.** JavaScript ve birçok API milisaniye
  kullanıyor: `1710000000123` gibi. Önce 1000'e böl. Bölmeyi unutursan Python
  56 bin yıl sonrasını hesaplamaya çalışıp hata veriyor.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| `date(9, 3, 2024)` | Hata ya da yanlış tarih | Sıra yıl, ay, gün |
| `%m` ile `%M`'yi karıştırmak | Ay yerine dakika okunuyor | `%m` ay, `%M` dakika |
| `%d/%m` ile `%m/%d`'yi karıştırmak | Sessizce yanlış tarih | Günü 12'den büyük satırla doğrula |
| Ay için `timedelta(days=30)` | Yanlış gün | Takvim ofseti (Bölüm 04) |
| Haftayı `isocalendar`'dan, yılı `.year`'dan almak | Var olmayan hafta | İkisini de `isocalendar`'dan al |
| Yaz saatli bölgede duvar saatiyle süre hesabı | Bir saat eksik ya da fazla | UTC'ye çevirip çıkar |
| `fromtimestamp` içinde dilim yazmamak | Makineye göre değişen sonuç | `tz=timezone.utc` |

## Özet

- Tarih metin değil bir **tür**: `date`, `datetime`, `time`, süreler için
  `timedelta`. Geçersiz tarih kurulamıyor.
- Sıra her zaman **yıl, ay, gün**. `weekday()` pazartesi 0, `isoweekday()`
  pazartesi 1.
- Tarih - tarih = süre; tarih + süre = tarih. `timedelta` ay ve yıl bilmiyor.
- **`strptime`** metni okur, **`strftime`** metne yazar; ISO metin için
  `fromisoformat`. `03/09/2024` gibi biçimler belirsiz.
- ISO haftası yıl sınırında başka yıla düşebiliyor; yılı da
  `isocalendar()`'dan al.
- Saat dilimsiz (naive) ve dilimli (aware) zaman var. **UTC'de sakla ve
  hesapla**, yerel saate yalnızca gösterirken çevir. Yaz saati geçişinde
  duvar saatine göre "1 gün" gerçekte 23 saat.
- Unix zamanı 1970'ten bu yana saniye; `tz=timezone.utc` ile çevir, 13 haneli
  sayıyı 1000'e böl.
