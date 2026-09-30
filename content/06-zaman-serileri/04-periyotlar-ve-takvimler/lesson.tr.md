# Periyotlar ve Takvimler

Şimdiye kadar her zaman damgası bir **noktaydı**: `2024-03-09`, ya da
`2024-03-09 14:30`. Ama "Mart 2024" bir nokta değil, 31 gün süren bir
**aralık**. "İlk çeyrek", "10. hafta", "2024 yılı" da öyle.

Takvim ayrıca düzgün de değil: aylar 28 ile 31 gün arasında değişiyor, hafta
sonları var, tatiller var. "Bir ay sonra", "üç iş günü sonra", "ayın son
günü" gibi sorular sabit bir süreyle cevaplanamıyor.

Bu bölüm takvimin bu iki yüzünü ele alıyor: **aralıklar** ve **takvime göre
hesap.**

## An ve aralık

<figure class="fig">
  <div class="versus">
    <div><h4><code>Timestamp</code>: an</h4><p>Takvimde tek bir <b>nokta</b>.<br><code>2024-03-09</code><br>"Ne zaman oldu?"</p></div>
    <div class="ok"><h4><code>Period</code>: aralık</h4><p>Başı ve sonu olan bir <b>dönem</b>.<br><code>2024-03</code> = 1 Mart 00:00 → 31 Mart 23:59<br>"Hangi dönemde oldu?"</p></div>
  </div>
  <figcaption>Günlük satış bir günün içinde birikiyor, aylık satış bir ayın içinde. Toplamları anlatırken aralık, olayları anlatırken nokta daha doğru bir dil.</figcaption>
</figure>

```python
import pandas as pd

p = pd.Period("2024-03", freq="M")

print(p)                 # 2024-03
print(p.start_time)      # 2024-03-01 00:00:00
print(p.end_time)        # 2024-03-31 23:59:59.999999
print(p.days_in_month)   # 31
print(p + 1)             # 2024-04
```

`Period` bir aralığı başı ve sonuyla tutuyor; `+ 1` bir sonraki aralığa
geçiyor. Bir günün hangi aralığa düştüğünü `to_period` söylüyor:

```python
day = pd.Timestamp("2024-03-09")

print(day.to_period("M"))   # 2024-03
print(day.to_period("Q"))   # 2024Q1
print(day.to_period("Y"))   # 2024
print(day.to_period("W"))   # 2024-03-04/2024-03-10
```

**Dikkat: periyotta `"M"`, `date_range`'de `"ME"`.** Geçen bölümde `"M"`
yazınca hata almıştın; burada tam tersi:

```python
pd.Period("2024-03", freq="ME")
# ValueError: Invalid frequency: ME ... for Period, please use 'M'
```

Mantığı şu: `"ME"` bir **nokta** (ayın son günü), `"M"` bir **aralık** (ayın
tamamı). Periyot aralıkla çalıştığı için `M`, `Q`, `Y` istiyor.

## Aylık toplamlar

Günlük seriyi aylara toplamanın en doğrudan yolu, her günü ait olduğu aya
atayıp gruplamak:

```python
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

monthly = s.groupby(s.index.to_period("M")).sum()

print(len(monthly))                  # 36
print(monthly.loc["2024-01":"2024-04"])
```

```text
date
2024-01    9103
2024-02    8491
2024-03    8919
2024-04    8003
Freq: M, Name: sales, dtype: int64
```

İndeks artık bir `PeriodIndex`: her satır bir gün değil, bir ay. Tarihle seçme
aynı şekilde çalışıyor (`monthly.loc["2024-03"]` → 8919). En yüksek ay
`monthly.idxmax()` → `2024-12`, 11335.

Bölüm 05'te aynı işi `resample` ile de yapacağız; o daha esnek. `to_period`
ise **bir tarihin hangi döneme ait olduğunu** söylemenin en açık yolu ve
gruplamada, etiketlemede hep işe yarıyor.

## Aylar eşit uzunlukta değil

Tabloya tekrar bak: Şubat'ın toplamı (8491) Mart'tan (8919) düşük. Şubat'ta
satışlar kötü mü gitti?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Ocak 2024</span><span>toplam <b>9103</b> · 31 gün · günde <b>293.6</b></span></div>
    <div class="anat-row"><span>Şubat 2024</span><span>toplam <b>8491</b> · 29 gün · günde <b>292.8</b></span></div>
    <div class="anat-row"><span>Mart 2024</span><span>toplam <b>8919</b> · 31 gün · günde <b>287.7</b></span></div>
    <div class="anat-row"><span>Nisan 2024</span><span>toplam <b>8003</b> · 30 gün · günde <b>266.8</b></span></div>
  </div>
  <figcaption>Toplama bakınca Şubat, Mart'ın gerisinde. Günlük ortalamaya bakınca önünde. Aradaki fark satıştan değil, takvimden geliyor.</figcaption>
</figure>

**Hayır.** Şubat 29 gün, Mart 31 gün. Günlük ortalamaya bakınca sıra tersine
dönüyor: Şubat **292.8**, Mart **287.7**. Şubat'ın toplamı düşük çünkü iki
gün kısa; mağaza o ay günde daha çok satmış.

```python
daily_mean = s.groupby(s.index.to_period("M")).mean().round(1)
days = monthly.index.days_in_month
```

Bu, zaman serisinin en sık yapılan okuma hatalarından biri. **Aylık toplamları
karşılaştırmadan önce gün sayısına böl.** Ay uzunluğu %10'a kadar fark
yaratıyor (28 ile 31 gün); gerçek değişim çoğu zaman bundan küçük.

## Çeyrekler ve haftalar

```python
quarterly = s.groupby(s.index.to_period("Q")).sum()
print(quarterly.loc["2024"])
```

```text
2024Q1    26513
2024Q2    24146
2024Q3    26025
2024Q4    30927
```

Haftalık periyot pazartesi başlayıp pazar bitiyor ve etiketi iki ucu
gösteriyor: `2024-03-04/2024-03-10`. Bölüm 01'deki ISO haftasıyla aynı
sınırlar, ama yıl sonu karışıklığı yok: etiket doğrudan tarihleri yazıyor.

Bazı şirketlerin mali yılı Ocak'ta başlamıyor. Mart'ta biten bir mali yıl için
`to_period("Q-MAR")`: 9 Mart 2024 `2024Q4`, 9 Nisan 2024 `2025Q1`.

## Periyottan tarihe geri

Grafik çizmek ya da başka bir tarih indeksli seriyle birleştirmek için
periyodu yeniden noktaya çevirmek gerekebiliyor:

```python
monthly.to_timestamp()             # ay baslari: 2022-01-01, 2022-02-01, ...
monthly.to_timestamp(how="end")    # ay sonlari
```

Bir ayı hangi günle temsil edeceğin bir tercih: ay başı mı, ay sonu mu?
Hangisini seçtiğini bil ve karıştırma; aylık iki seriyi birleştirirken biri ay
başında, öteki ay sonundaysa **hiçbir satır eşleşmiyor.**

## Takvime göre ileri geri: `DateOffset`

Bölüm 01'de `timedelta`'nın ay bilmediğini gördün. pandas'taki karşılığı
`DateOffset`:

<figure class="fig">
  <div class="versus">
    <div><h4><code>Timedelta</code>: süre</h4><p>Sabit uzunluk: gün, saat, dakika.<br><code>31 Oca + 30 gün</code> → <b>1 Mart</b><br>Süre ölçerken.</p></div>
    <div class="ok"><h4><code>DateOffset</code>: takvim</h4><p>Ay ve yıl biliyor.<br><code>31 Oca + 1 ay</code> → <b>29 Şub</b><br>Takvimde ilerlerken.</p></div>
  </div>
  <figcaption>"Bir ay sonra" 28, 29, 30 ya da 31 gün olabiliyor. Hangisi olduğunu takvim biliyor, süre bilmiyor.</figcaption>
</figure>

```python
t = pd.Timestamp("2024-01-31")

print(t + pd.Timedelta(days=30))        # 2024-03-01   30 gun sonra
print(t + pd.DateOffset(months=1))      # 2024-02-29   bir ay sonra
```

Şubat'ta 31. gün olmadığı için `DateOffset` ayın **son geçerli gününe**
iniyor. Aynı kural başka yerlerde de:

```python
pd.Timestamp("2024-03-31") + pd.DateOffset(months=1)    # 2024-04-30
pd.Timestamp("2024-02-29") + pd.DateOffset(years=1)     # 2025-02-28
pd.Timestamp("2024-03-09") - pd.DateOffset(years=1)     # 2023-03-09   gecen yil ayni gun
```

Son satır çok kullanılacak: "geçen yılın aynı günü" ile karşılaştırmak yıllık
mevsimselliği dışarıda bırakmanın en basit yolu.

## Ay sonu, ay başı

Bir tarihi takvimdeki belirli bir noktaya **taşımak** için hazır ofsetler var:

```python
from pandas.tseries.offsets import MonthEnd, MonthBegin

d = pd.Timestamp("2024-03-09")

print(d + MonthEnd(0))      # 2024-03-31   bu ayin sonu
print(d + MonthEnd(1))      # 2024-03-31   bir sonraki ay sonu (yine bu ay)
print(d - MonthBegin(1))    # 2024-03-01   bu ayin basi
print(d + MonthBegin(1))    # 2024-04-01   gelecek ayin basi
```

`MonthEnd(0)` "zaten ay sonundaysan kıpırdama, değilsen ay sonuna git" demek.
`MonthEnd(1)` ise ay sonundaysan bir sonraki ay sonuna atlıyor
(`2024-03-31 + MonthEnd(1)` → `2024-04-30`). Aradaki fark yalnızca tarih tam
ay sonuna denk geldiğinde görünüyor ve tam da bu yüzden kolay kaçıyor.

Bütün indekse uygulanınca "ay sonuna kaç gün kaldı" gibi bir özellik
çıkıyor:

```python
days_left = ((s.index + MonthEnd(0)) - s.index).days     # 30, 29, 28, ...
```

Maaş günü, fatura günü, ay sonu kapanışı olan işlerde satış bu sayıya bağlı
hareket ediyor.

## İş günleri

Birçok seri yalnızca iş günlerinde var: borsa, banka işlemleri, ofis
trafiği. `BDay` (business day) hafta sonlarını atlıyor:

```python
from pandas.tseries.offsets import BDay

friday = pd.Timestamp("2024-03-08")

print(friday + BDay(1))                 # 2024-03-11   pazartesi
print(friday + BDay(3))                 # 2024-03-13   carsamba
print(len(pd.bdate_range("2024-03-01", "2024-03-31")))    # 21
print(len(pd.bdate_range("2024-01-01", "2024-12-31")))    # 262
```

Ayların iş günü sayısı da eşit değil:

<figure class="fig">
  <svg viewBox="0 0 680 220" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="190.0" x2="666" y2="190.0"/><text class="dim" x="38" y="193.5" font-size="10.5" text-anchor="end">18</text><line class="grid" x1="44" y1="162.7" x2="666" y2="162.7"/><text class="dim" x="38" y="166.2" font-size="10.5" text-anchor="end">19</text><line class="grid" x1="44" y1="135.3" x2="666" y2="135.3"/><text class="dim" x="38" y="138.8" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="108.0" x2="666" y2="108.0"/><text class="dim" x="38" y="111.5" font-size="10.5" text-anchor="end">21</text><line class="grid" x1="44" y1="80.7" x2="666" y2="80.7"/><text class="dim" x="38" y="84.2" font-size="10.5" text-anchor="end">22</text><line class="grid" x1="44" y1="53.3" x2="666" y2="53.3"/><text class="dim" x="38" y="56.8" font-size="10.5" text-anchor="end">23</text><line class="grid" x1="44" y1="26.0" x2="666" y2="26.0"/><text class="dim" x="38" y="29.5" font-size="10.5" text-anchor="end">24</text><line class="line" x1="44" y1="190" x2="666" y2="190"/><line class="line" x1="74.6" y1="190" x2="74.6" y2="194"/><text class="dim" x="74.6" y="206" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="125.6" y1="190" x2="125.6" y2="194"/><text class="dim" x="125.6" y="206" font-size="10.5" text-anchor="middle">Şub</text><line class="line" x1="176.6" y1="190" x2="176.6" y2="194"/><text class="dim" x="176.6" y="206" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="227.5" y1="190" x2="227.5" y2="194"/><text class="dim" x="227.5" y="206" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="278.5" y1="190" x2="278.5" y2="194"/><text class="dim" x="278.5" y="206" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="329.5" y1="190" x2="329.5" y2="194"/><text class="dim" x="329.5" y="206" font-size="10.5" text-anchor="middle">Haz</text><line class="line" x1="380.5" y1="190" x2="380.5" y2="194"/><text class="dim" x="380.5" y="206" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="431.5" y1="190" x2="431.5" y2="194"/><text class="dim" x="431.5" y="206" font-size="10.5" text-anchor="middle">Ağu</text><line class="line" x1="482.5" y1="190" x2="482.5" y2="194"/><text class="dim" x="482.5" y="206" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="533.4" y1="190" x2="533.4" y2="194"/><text class="dim" x="533.4" y="206" font-size="10.5" text-anchor="middle">Eki</text><line class="line" x1="584.4" y1="190" x2="584.4" y2="194"/><text class="dim" x="584.4" y="206" font-size="10.5" text-anchor="middle">Kas</text><line class="line" x1="635.4" y1="190" x2="635.4" y2="194"/><text class="dim" x="635.4" y="206" font-size="10.5" text-anchor="middle">Ara</text><rect class="dot" x="58.8" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="109.8" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="160.8" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="211.7" y="80.7" width="31.6" height="109.3" rx="3" opacity="0.9"/><rect class="dot" x="262.7" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="313.7" y="135.3" width="31.6" height="54.7" rx="3" opacity="0.9"/><rect class="dot" x="364.7" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="415.7" y="80.7" width="31.6" height="109.3" rx="3" opacity="0.9"/><rect class="dot" x="466.7" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="517.6" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="568.6" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="619.6" y="80.7" width="31.6" height="109.3" rx="3" opacity="0.9"/><text class="ink" x="74.6" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="125.6" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="176.6" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="227.5" y="73.8" font-size="11" text-anchor="middle">22</text><text class="ink" x="278.5" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="329.5" y="128.5" font-size="11" text-anchor="middle">20</text><text class="ink" x="380.5" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="431.5" y="73.8" font-size="11" text-anchor="middle">22</text><text class="ink" x="482.5" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="533.4" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="584.4" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="635.4" y="73.8" font-size="11" text-anchor="middle">22</text></svg>
  <figcaption>2024'te aylara göre iş günü sayısı (pazartesi–cuma, tatiller sayılmadan). En az Haziran'da 20, en çok 23. Dikey eksen 18'den başlıyor.</figcaption>
</figure>

Haziran 20, Ocak 23 iş günü: **%15 fark.** Yalnızca iş günlerinde gerçekleşen
bir şeyin (fatura sayısı, üretim) aylık toplamı, hiçbir şey değişmese bile bu
kadar oynuyor.

Hisse fiyatı serisi (`stock_price.csv`) bunun örneği: 782 satır, hepsi hafta
içi.

```python
close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

print(pd.infer_freq(close.index))           # B
print(close.asfreq("D").isna().sum())       # 312
```

Bu seriyi `asfreq("D")` ile günlük takvime oturtursan 312 tane "eksik" gün
çıkıyor. Hiçbiri eksik değil: borsa o günler kapalıydı. **Serinin kendi
frekansını kullan** (`"B"`); hafta sonlarını eksik veri sanıp doldurmak
olmayan fiyatlar uydurmak olur.

## Tatiller

`BDay` yalnızca hafta sonlarını biliyor. Resmi tatilleri bilmiyor, çünkü
tatiller ülkeden ülkeye değişiyor. Listeyi sen veriyorsun:

```python
from pandas.tseries.offsets import CustomBusinessDay

holidays = pd.read_csv("holidays_2024.csv", parse_dates=["date"])["date"]
workday = CustomBusinessDay(holidays=holidays)

print(len(pd.date_range("2024-01-01", "2024-12-31", freq=workday)))    # 250
print(len(pd.date_range("2024-04-01", "2024-04-30", freq=workday)))    # 18
```

262 iş gününün 12'si tatile denk geliyor: **250 çalışma günü.** (14 tatilin
ikisi zaten pazara düşüyor.) Nisan ise 22 iş gününden 18'e iniyor: Ramazan
Bayramı üç günü, 23 Nisan bir günü götürüyor.

Fark teslim tarihi gibi hesaplarda somutlaşıyor. 9 Nisan Salı günü verilen
siparişe "3 iş günü" söz verildi:

```python
order = pd.Timestamp("2024-04-09")

print(order + BDay(3))        # 2024-04-12   bayramin ucuncu gunu!
print(order + 3 * workday)    # 2024-04-17
```

Tatil takvimi olmadan söz verilen gün, kimsenin çalışmadığı bir gün.

Tatili bir **özellik** olarak kullanmak da tek satır:

```python
is_holiday = s.index.isin(holidays)
```

Hafta sonu cuma–cumartesi olan ülkeler için
`CustomBusinessDay(weekmask="Sun Mon Tue Wed Thu")`.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| `Period(..., freq="ME")` | `Invalid frequency` | Periyotta `M`, `Q`, `Y` |
| Aylık toplamları doğrudan karşılaştırmak | Kısa ay "kötü" görünüyor | Gün (ya da iş günü) sayısına böl |
| "Bir ay sonra" için `Timedelta(days=30)` | Yanlış gün | `pd.DateOffset(months=1)` |
| `MonthEnd(1)` ile `MonthEnd(0)`'ı karıştırmak | Ay sonundaki tarih bir ay ileri gidiyor | "Bu ayın sonu" için `MonthEnd(0)` |
| İş günü serisini `asfreq("D")` yapmak | Hafta sonları "eksik" görünüyor | `asfreq("B")` |
| Tatilsiz `BDay` ile tarih sözü vermek | Tatil gününe denk geliyor | `CustomBusinessDay(holidays=...)` |
| Ay başı ile ay sonu temsilini karıştırmak | Birleştirmede satırlar eşleşmiyor | Birini seç, her yerde onu kullan |

## Özet

- `Timestamp` bir **an**, `Period` bir **aralık**. `to_period("M")` bir günün
  hangi aya düştüğünü söylüyor.
- Periyotta kısaltmalar `M`, `Q`, `Y`, `W`; `date_range`'deki `ME` burada
  çalışmıyor.
- `s.groupby(s.index.to_period("M")).sum()` aylık toplam; `to_timestamp()`
  periyodu tarihe geri çeviriyor.
- **Aylar eşit değil.** Karşılaştırmadan önce gün ya da iş günü sayısına böl.
- `DateOffset` takvime göre ilerliyor (ay, yıl); `MonthEnd`, `MonthBegin`
  tarihi takvimdeki bir noktaya taşıyor.
- `BDay` hafta sonlarını atlıyor; tatiller için `CustomBusinessDay` ve kendi
  tatil listen. İş günü serisinin frekansı `B`.
