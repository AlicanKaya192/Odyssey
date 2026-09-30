# pandas'ta Tarihler

Geçen bölümde tek tek tarihlerle çalıştın. Gerçek veride tarih bir
**sütun**: binlerce satır, hepsi dosyadan metin olarak geliyor. Bu bölümde o
sütunu gerçek tarihe çeviriyoruz, bozuk satırları yakalıyoruz ve tarihin
parçalarına (yıl, ay, haftanın günü) tek satırla ulaşıyoruz.

Kurallar Bölüm 01'dekilerin aynısı; yalnızca artık her işlem bütün sütuna
birden uygulanıyor.

## Metin mi, tarih mi?

`read_csv` tarihleri kendiliğinden tarih yapmıyor. Dosyayı okuduktan sonra ilk
bakılacak yer `dtypes`:

```python
import pandas as pd

sales = pd.read_csv("store_sales.csv")
print(sales.dtypes)
```

```text
date       str
sales    int64
```

`date` sütunu **metin** (`str`; eski pandas sürümlerinde `object` yazıyor).
Metin üzerinde tarih işlemi yapılamıyor:

```python
sales["date"].dt.year
# AttributeError: Can only use .dt accessor with datetimelike values
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Metin (<code>str</code>)</h4><p>Yalnızca harf dizisi.<br><code>.dt</code> çalışmıyor.<br>Karşılaştırma alfabetik.<br>İki tarih çıkarılamıyor.</p></div>
    <div class="ok"><h4>Tarih (<code>datetime64</code>)</h4><p>Takvimi biliyor.<br><code>.dt.year</code>, <code>.dt.day_name()</code>.<br>Karşılaştırma zamana göre.<br>Fark bir süre veriyor.</p></div>
  </div>
  <figcaption>Ekranda ikisi de <code>2022-01-01</code> diye görünüyor. Farkı yalnızca <code>dtypes</code> gösteriyor.</figcaption>
</figure>

## `to_datetime`

```python
sales["date"] = pd.to_datetime(sales["date"])
print(sales.dtypes)
```

```text
date     datetime64[us]
sales             int64
```

`datetime64` pandas'ın tarih türü; köşeli parantezdeki `us` çözünürlük
(mikrosaniye). Artık sütun takvimi biliyor:

```python
print(sales["date"].min())                              # 2022-01-01 00:00:00
print(sales["date"].max())                              # 2024-12-31 00:00:00
print((sales["date"].max() - sales["date"].min()).days) # 1095
```

Dosyayı okurken tek adımda da yapılabiliyor:

```python
sales = pd.read_csv("store_sales.csv", parse_dates=["date"])
```

**Çevirdikten sonra `dtypes`'a tekrar bak.** Çevirme başarısız olduğunda pandas
bazen sütunu sessizce metin bırakıyor; bunu fark etmenin tek yolu bakmak.

## `Timestamp`: tek bir an

Sütunun her elemanı bir `Timestamp`. Python'daki `datetime`'ın pandas
karşılığı; aynı özellikleri taşıyor, üstüne birkaç tane daha ekliyor:

```python
t = pd.Timestamp("2024-03-09 14:37")

print(t.year, t.month, t.day_name())    # 2024 3 Saturday
print(t + pd.Timedelta("2h 15min"))     # 2024-03-09 16:52:00
print(t.normalize())                    # 2024-03-09 00:00:00   saati sifirla
print(t.floor("h"))                     # 2024-03-09 14:00:00   asagi yuvarla
print(t.round("15min"))                 # 2024-03-09 14:30:00   en yakina
```

`normalize()`, `floor` ve `round` ileride çok işe yarayacak: aynı güne ya da
aynı saate düşen kayıtları bir araya getirmenin yolu bunlar.

## Gün önde yazılmış tarihler: sessiz hata

ISO biçimi (`2024-03-09`) sorunsuz okunuyor. Dünyanın büyük kısmı ise tarihi
gün önde yazıyor: `09.03.2024`. Biçim söylenmezse pandas **ilk satıra bakıp
tahmin ediyor** ve tahmini ay-gün-yıl:

```python
dates = pd.Series(["09.03.2024", "10.03.2024", "11.03.2024"])
print(pd.to_datetime(dates))
```

```text
0   2024-09-03
1   2024-10-03
2   2024-11-03
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>09.03.2024</code></span><span>pandas: <b>3 Eylül</b> · gerçek: 9 Mart</span></div>
    <div class="anat-row"><span><code>10.03.2024</code></span><span>pandas: <b>3 Ekim</b> · gerçek: 10 Mart</span></div>
    <div class="anat-row"><span><code>11.03.2024</code></span><span>pandas: <b>3 Kasım</b> · gerçek: 11 Mart</span></div>
    <div class="anat-row"><span><code>13.03.2024</code></span><span>13. ay yok: ancak burada <b>hata</b> çıkıyor</span></div>
  </div>
  <figcaption>Biçim söylenmeyince ilk sayı ay sanılıyor. Günü 12'yi geçmeyen tarihlerde bu hata görünmez kalıyor.</figcaption>
</figure>

**Hata yok, uyarı yok, sonuç yanlış.** 9, 10 ve 11 Mart; 3 Eylül, 3 Ekim ve
3 Kasım oldu. Bütün günler 12 ya da daha küçük olduğu sürece pandas bunu fark
edemiyor.

Günü 12'den büyük bir satır gelince tahmin tutmuyor ve ancak o zaman hata
çıkıyor:

```python
pd.to_datetime(pd.Series(["09.03.2024", "13.03.2024"]))
# ValueError: time data "13.03.2024" doesn't match format "%m.%d.%Y"
```

Çözüm, Bölüm 01'deki kodlarla **biçimi açıkça yazmak**:

```python
pd.to_datetime(dates, format="%d.%m.%Y")
```

```text
0   2024-03-09
1   2024-03-10
2   2024-03-11
```

`dayfirst=True` da aynı işi görüyor, ama `format` iki açıdan daha iyi: biçime
uymayan satırda hata veriyor (yanlış veriyi erken yakalıyorsun) ve büyük
dosyalarda daha hızlı. **Kural: tarih ISO değilse her zaman `format` yaz.**

## Bozuk tarihler: `errors="coerce"` ve `NaT`

Gerçek dosyalarda bazı satırlar tarih bile değil. Sipariş tablosuna bakalım
(`orders_raw.csv`, 240 satır):

```text
order_id       ordered_at delivered_on  amount
   A1000 03.01.2024 05:12   2024-01-07  225.73
   A1001 04.01.2024 16:13   2024-01-05   63.12
   A1002 05.01.2024 01:24   2024-01-07   35.04
```

```python
orders = pd.read_csv("orders_raw.csv")
pd.to_datetime(orders["ordered_at"], format="%d.%m.%Y %H:%M")
# ValueError: day 31 must be in range 1..29 for month 2 in year 2024
```

Tek bir bozuk satır bütün çevirmeyi durduruyor. `errors="coerce"` bozuk
satırları **`NaT`** (Not a Time; tarihlerin `NaN`'ı) yapıp devam ediyor:

```python
ordered = pd.to_datetime(orders["ordered_at"],
                         format="%d.%m.%Y %H:%M", errors="coerce")

print(ordered.isna().sum())                        # 3
print(orders.loc[ordered.isna(), "ordered_at"].tolist())
# ['31.02.2024 10:15', 'unknown', '00.00.0000 00:00']
```

İkinci satır önemli: **`coerce`'u körlemesine kullanma.** Önce kaç satırın ve
**hangilerinin** bozuk olduğuna bak. 240 satırda 3 tanesi bozuksa onları
atarsın; 120 tanesi `NaT` olduysa sorun satırlarda değil, senin yazdığın
biçimde.

`NaT` de `NaN` gibi davranıyor: hiçbir şeye eşit değil (kendine bile),
karşılaştırmaları `False`, toplama ve ortalamada atlanıyor. `isna()`,
`dropna()` ve `fillna()` onunla da çalışıyor.

## `.dt`: tarihin parçaları

Tarih sütununda `.dt` ile her satırın parçasına tek seferde ulaşılıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>.dt.year</code> <code>.dt.month</code> <code>.dt.day</code></span><span>Yıl, ay, gün (sayı)</span></div>
    <div class="anat-row"><span><code>.dt.dayofweek</code></span><span>Haftanın günü: pazartesi 0 ... pazar 6</span></div>
    <div class="anat-row"><span><code>.dt.day_name()</code></span><span>Günün adı: <code>Saturday</code></span></div>
    <div class="anat-row"><span><code>.dt.quarter</code></span><span>Çeyrek: 1–4</span></div>
    <div class="anat-row"><span><code>.dt.hour</code></span><span>Saat: 0–23</span></div>
    <div class="anat-row"><span><code>.dt.normalize()</code></span><span>Saati gece yarısına çekilmiş tarih</span></div>
  </div>
  <figcaption>Hepsi sütunun tamamına uygulanıyor ve satır sayısı kadar değer veriyor. Tam liste ".dt Başvurusu" notunda.</figcaption>
</figure>

```python
sales["weekday"] = sales["date"].dt.day_name()
print(sales.groupby("weekday")["sales"].mean().round(1).sort_values(ascending=False))
```

```text
weekday
Saturday     336.1
Sunday       296.9
Friday       278.9
Thursday     241.1
Wednesday    228.6
Tuesday      220.6
Monday       217.6
```

Bölüm 00'da bunu hazır bir `weekday` sütunuyla yapmıştık; artık kendin
üretiyorsun. Hafta sonunun payı da tek satır:

```python
weekend = sales["date"].dt.dayofweek >= 5
print(round(sales.loc[weekend, "sales"].sum() / sales["sales"].sum() * 100, 1))   # 34.9
```

Haftanın 7 gününden 2'si, satışın **%34.9'u.**

## Tarihe göre süzmek

Tarih sütunu metinle yazılmış bir tarihle doğrudan karşılaştırılabiliyor;
pandas metni kendisi çeviriyor:

```python
sales[sales["date"] >= "2024-12-01"]                       # 31 satir
sales[sales["date"].between("2024-03-04", "2024-03-10")]   # 7 satir

march = (sales["date"].dt.year == 2024) & (sales["date"].dt.month == 3)
print(sales.loc[march, "sales"].sum())                     # 8919
```

`between` iki ucu da dahil ediyor. Bu yalnızca sütun **gerçek tarihken** doğru
çalışıyor; metin sütununda aynı satır alfabetik karşılaştırma yapıyor ve gün
önde yazılmış tarihlerde yanlış satırları getiriyor.

## Süre sütunu

İki tarih sütununun farkı bir **süre sütunu** (`timedelta64`):

```python
delivered = pd.to_datetime(orders["delivered_on"], errors="coerce")
days = (delivered - ordered.dt.normalize()).dt.days

print(days.notna().sum())        # 230
print(round(days.mean(), 2))     # 2.33
print(days.max())                # 8.0
print((days > 3).sum())          # 33
```

Üç ayrıntı:

- `delivered_on` yalnızca gün içeriyor, `ordered_at` saat de içeriyor.
  `normalize()` sipariş saatini gece yarısına çekiyor ki fark **tam gün**
  çıksın.
- Süre sütununda da `.dt` var: `.dt.days`, `.dt.total_seconds()`.
- Taraflardan biri `NaT` ise fark da `NaT`. 240 siparişin 230'unda iki tarih
  de geçerli; ortalama yalnızca onlardan hesaplandı.

## Saat dilimleri

Bir sensörün kayıtları UTC ile gelmiş (`Z` harfi UTC demek):

```text
            time_utc  temp_c
2024-03-29T23:00:00Z    16.4
2024-03-30T00:00:00Z    16.9
```

```python
sensor = pd.read_csv("berlin_sensor.csv")
sensor["time_utc"] = pd.to_datetime(sensor["time_utc"])
print(sensor["time_utc"].dtype)            # datetime64[us, UTC]

local = sensor["time_utc"].dt.tz_convert("Europe/Berlin")
print(local.dt.date.value_counts().sort_index())
```

```text
2024-03-30    24
2024-03-31    23
2024-04-01    24
```

**31 Mart 23 satır.** Bölüm 01'deki yaz saati geçişi, burada tablonun içinde:
o günün bir saati yok. Günlük ortalama alırsan sorun olmuyor; günlük
**toplam** alırsan o gün bir saat eksik toplanıyor.

İki işlem var ve Bölüm 01'deki `replace` / `astimezone` ayrımının aynısı:

<figure class="fig">
  <div class="versus">
    <div><h4><code>tz_localize</code>: tanıt</h4><p>Dilimsiz sütuna "bu saatler şu dilimde" diyorsun.<br><b>Saat değişmiyor</b>, yalnızca etiket ekleniyor.<br><code>14:30</code> → <code>14:30+03:00</code></p></div>
    <div><h4><code>tz_convert</code>: dönüştür</h4><p>Dilimli sütunu başka dilimin saatiyle gösteriyorsun.<br><b>Saat değişiyor</b>, an aynı kalıyor.<br><code>14:30+03:00</code> → <code>11:30+00:00</code></p></div>
  </div>
  <figcaption>Dilimsiz sütunda <code>tz_convert</code> hata veriyor: neyi neye çevireceğini bilmiyor. Önce tanıt, sonra dönüştür.</figcaption>
</figure>

Dilimsiz bir sütunu yaz saati uygulanan bir bölgeye tanıtırken pandas olmayan
saati görünce duruyor:

```python
naive = pd.Series(pd.to_datetime(["2024-03-31 01:30", "2024-03-31 02:30"]))
naive.dt.tz_localize("Europe/Berlin")
# ValueError: 2024-03-31 02:30:00 is a nonexistent time due to daylight savings time
```

Ne yapılacağını sen söylüyorsun: `nonexistent="shift_forward"` (03:00'e
kaydır) ya da `nonexistent="NaT"`. Sonbaharda iki kez yaşanan saat için
karşılığı `ambiguous=`. En temiz yol yine aynı: **veriyi UTC olarak tut.**

## Unix zamanı sütunu

Sayı olarak gelen zamanlar için birimi söylemek yetiyor:

```python
pd.to_datetime(events["ts"], unit="s", utc=True)     # saniye
pd.to_datetime(events["ts"], unit="ms", utc=True)    # milisaniye
```

`unit` yazmazsan pandas sayıyı **nanosaniye** sayıyor ve her şey 1970'in ilk
saniyelerine düşüyor. Sonuçta bütün tarihler `1970-01-01` görünüyorsa sebep
bu.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Çevirmeden `.dt` kullanmak | `AttributeError` | Önce `to_datetime`, sonra `dtypes`'a bak |
| Gün önde tarihi biçimsiz okumak | Sessizce ay ile gün yer değiştiriyor | `format="%d.%m.%Y"` |
| `errors="coerce"` yazıp bakmamak | Verinin yarısı `NaT` olabilir | `isna().sum()` ve bozuk satırları yazdır |
| Metin sütununu tarihle karşılaştırmak | Alfabetik karşılaştırma | Önce çevir |
| Saatli ve saatsiz tarihi doğrudan çıkarmak | Kesirli, yanıltıcı gün sayısı | `normalize()` |
| `tz_localize` ile `tz_convert`'i karıştırmak | An değişiyor | Tanıtmak için `localize`, dönüştürmek için `convert` |
| Unix sütununda `unit` yazmamak | Bütün tarihler 1970 | `unit="s"` ya da `"ms"` |

## Özet

- Dosyadan gelen tarih **metindir.** `pd.to_datetime` (ya da
  `read_csv(parse_dates=...)`) ile çevir, sonra `dtypes`'a bak.
- Tarih ISO değilse **`format` yaz.** Yazmazsan gün önde tarihler sessizce
  yanlış okunabiliyor.
- `errors="coerce"` bozuk satırları `NaT` yapıyor; kaç tane ve hangileri
  olduğuna mutlaka bak.
- `.dt` tarihin parçalarını veriyor: `year`, `month`, `dayofweek`,
  `day_name()`, `normalize()`.
- Tarih sütunu metin tarihlerle süzülebiliyor: `>=`, `between`.
- İki tarih sütununun farkı süre sütunu: `.dt.days`, `.dt.total_seconds()`.
- `tz_localize` dilimi tanıtıyor, `tz_convert` dönüştürüyor. Yaz saati günü
  saatlik veride 23 ya da 25 satır.
