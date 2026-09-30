# Zaman İndeksi

Geçen bölümde tarih bir **sütundu**. Bu bölümde onu tablonun **indeksine**
alıyoruz. Küçük bir değişiklik gibi duruyor ama pandas'ın zaman serisi
araçlarının hepsi buna bakıyor: tarihle seçmek, bir ayı tek kelimeyle almak,
eksik günleri bulmak ve sonraki bölümlerde göreceğin yeniden örnekleme,
kaydırma, hareketli pencere.

Tarih indekste olduğunda pandas tabloyu bir zaman serisi olarak görüyor.

## Tarihi indekse almak

```python
import pandas as pd

sales = pd.read_csv("store_sales.csv", parse_dates=["date"])
sales = sales.set_index("date")
s = sales["sales"]

print(type(s.index).__name__)   # DatetimeIndex
print(s.head(3))
```

```text
date
2022-01-01    305
2022-01-02    277
2022-01-03    201
Name: sales, dtype: int64
```

Okurken tek adımda da olur:

```python
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
```

`s` artık tek sütunlu bir seri: solda tarih, sağda değer. Patikanın geri
kalanında zaman serisini çoğunlukla bu biçimde tutacağız.

## Tarihle seçmek

Satır numarası yerine **tarih yazıyorsun**:

```python
print(s.loc["2024-03-09"])        # 384         tek gun
print(len(s.loc["2024-03"]))      # 31          butun Mart
print(s.loc["2024-03"].sum())     # 8919
print(len(s.loc["2024"]))         # 366         butun yil
print(round(s.loc["2024"].mean(), 1))   # 294.0
```

`"2024-03"` yazmak yetiyor; pandas bunu "Mart 2024'ün tamamı" diye anlıyor.
Geçen bölümde aynı toplamı `dt.year` ve `dt.month` ile iki koşul yazarak
bulmuştun; burada tek kelime.

## Dilimlemek

```python
week = s.loc["2024-03-04":"2024-03-10"]
print(len(week), week.sum())                        # 7 1978

print(len(s.loc["2024-01":"2024-03"]))              # 91   ilk ceyrek
print(len(s.loc[:"2022-01-07"]))                    # 7    bastan o gune
print(len(s.loc["2024-12-25":]))                    # 7    o gunden sona
```

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4><code>loc</code>: etiketle</h4><p><code>s.loc["2024-03-04":"2024-03-10"]</code><br>Tarih yazıyorsun.<br><b>İki uç da dahil</b>: 7 gün.</p></div>
    <div><h4><code>iloc</code>: konumla</h4><p><code>s.iloc[0:7]</code><br>Satır numarası yazıyorsun.<br><b>Son hariç</b>: 0'dan 6'ya 7 satır.</p></div>
  </div>
  <figcaption>Zaman serisinde çoğu zaman <code>loc</code> kullanılıyor: "Mart'ın ilk haftası" demek, "796. satırdan 803. satıra" demekten hem kolay hem güvenli.</figcaption>
</figure>

**Tarih dilimi iki ucu da dahil ediyor.** `"2024-03-04":"2024-03-10"` yedi gün
veriyor; `iloc[0:7]` ise 0'dan 6'ya yedi satır veriyor ve 7. satırı almıyor.
Tarihle çalışırken "son gün dahil mi?" diye düşünmene gerek yok: dahil.

Var olmayan tek bir gün hata, var olmayan bir aralık boş sonuç veriyor:

```python
s.loc["2025-01-01"]                       # KeyError
len(s.loc["2025-01-01":"2025-02-01"])     # 0
```

## İndeksin kendi parçaları

Sütunda `.dt` yazıyordun; indekste ona gerek yok:

```python
print(s.index.min(), s.index.max())     # 2022-01-01 ... 2024-12-31
print(s.index[-1] - s.index[0])         # 1095 days

weekend = s[s.index.dayofweek >= 5]
print(round(weekend.mean(), 1))         # 316.5

print(s.groupby(s.index.month).mean().round(1).loc[12])   # 327.3
```

`s.index.year`, `s.index.month`, `s.index.dayofweek`, `s.index.day_name()`...
Geçen bölümdeki `.dt` listesinin tamamı indekste doğrudan çalışıyor.

## Gerçek dosyalar dağınık

Şimdiye kadarki dosya temizdi. Aynı mağazanın 2024 kayıtları başka bir
sistemden şöyle gelmiş (`sales_messy.csv`, 362 satır):

```text
      date  sales
2024-04-13    351
2024-11-28    297
2024-07-22    232
2024-01-25    281
```

Üç ayrı sorun var: **sıra karışık, bazı günler iki kez yazılmış, bazı günler
hiç yok.** Hiçbiri tabloya bakınca görünmüyor; her birini ayrı bir soruyla
yakalıyoruz.

<figure class="fig">
  <div class="flow">
    <span class="node">Tarihi indekse al</span><span class="arrow">→</span>
    <span class="node">Sırala<br><code>sort_index()</code></span><span class="arrow">→</span>
    <span class="node">Tekrarları çöz<br><code>groupby(level=0)</code></span><span class="arrow">→</span>
    <span class="node">Eksikleri bul<br><code>date_range</code></span><span class="arrow">→</span>
    <span class="node acc">Takvime oturt<br><code>asfreq</code></span>
  </div>
  <figcaption>Yeni bir zaman serisiyle yapılacak ilk beş iş, bu sırayla. Sıra önemli: tekrar varken takvime oturtulamıyor, sırasızken dilimlenemiyor.</figcaption>
</figure>

### 1. Sıra

```python
messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]

print(messy.index.is_monotonic_increasing)     # False
messy.loc["2024-03-04":"2024-03-10"]
# KeyError: Value based partial slicing on non-monotonic DatetimeIndexes ...
```

Sıralı olmayan bir indekste tarih aralığı **seçilemiyor.** Çözüm tek satır:

```python
messy = messy.sort_index()
```

**Tarihi indekse aldıktan sonra her zaman `sort_index()` çağır.** Zararı yok,
sıralı veride hiçbir şey değiştirmiyor.

### 2. Tekrarlanan tarihler

```python
print(messy.index.is_unique)                   # False
print(messy.index.duplicated().sum())          # 4
print(messy.loc["2024-03-05"].tolist())        # [157, 105]
```

5 Mart için **iki satır** var. Tek bir gün isteyip iki değer almak, sonraki
her hesabı bozar. Ne yapılacağı verinin anlamına bağlı:

| Durum | Çözüm |
|---|---|
| Günün satışı iki parça hâlinde yazılmış | Topla: `groupby(level=0).sum()` |
| Aynı kayıt iki kez gelmiş | Birini at: `~index.duplicated()` |
| Sonradan düzeltilmiş değer gelmiş | Sonuncuyu al: `groupby(level=0).last()` |
| Aynı anın iki ölçümü | Ortalama: `groupby(level=0).mean()` |

Burada kayıtlar parça parça: 157 + 105 = 262, temiz dosyadaki gerçek değer.

```python
fixed = messy.groupby(level=0).sum()
print(len(fixed), fixed.index.is_unique)       # 358 True
```

`level=0` "indekse göre grupla" demek. **Hangisini seçeceğini pandas bilemez;
veriyi üreten sisteme sorman gerekiyor.** Yanlış seçim (parçaları toplamak
yerine birini atmak) o günün satışını yarıya indiriyor.

### 3. Eksik tarihler

358 satır var; 2024 ise 366 gün. Hangi günler yok?

```python
full = pd.date_range(fixed.index.min(), fixed.index.max(), freq="D")
missing = full.difference(fixed.index)

print(len(full), len(missing))                 # 366 8
print(missing.strftime("%Y-%m-%d").tolist())
```

```text
['2024-02-10', '2024-02-11', '2024-04-23', '2024-07-15', '2024-07-16',
 '2024-07-17', '2024-10-29', '2024-12-25']
```

`date_range` olması gereken tam takvimi üretiyor; `difference` elimizde
olmayanları veriyor.

Eksik gün neden bu kadar önemli? Çünkü zaman serisi araçları **"bir önceki
satır dün"** diye varsayıyor. 14 Temmuz'dan sonraki satır 18 Temmuz ise "dünle
bugünün farkı" aslında dört günün farkı oluyor ve hiçbir hata çıkmıyor.

## Frekans ve `asfreq`

Düzenli bir serinin **frekansı** var: günlük, saatlik, aylık. pandas bunu
indeksten tahmin edebiliyor:

```python
print(pd.infer_freq(s.index))        # D      temiz seri: gunluk
print(pd.infer_freq(fixed.index))    # None   eksik gunler yuzunden tahmin edemiyor
```

`asfreq("D")` seriyi tam günlük takvime oturtuyor; eksik günler için satır
açıp değerini **boş** (`NaN`) bırakıyor:

```python
regular = fixed.asfreq("D")

print(len(regular), regular.isna().sum())           # 366 8
print(regular.loc["2024-07-14":"2024-07-18"].tolist())
# [312.0, nan, nan, nan, 253.0]
```

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="324.9" y="14" width="60.2" height="186" opacity="0.8" style="stroke:none"/><line class="grid" x1="44" y1="185.0" x2="666" y2="185.0"/><text class="dim" x="38" y="188.5" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="134.4" x2="666" y2="134.4"/><text class="dim" x="38" y="137.9" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="83.7" x2="666" y2="83.7"/><text class="dim" x="38" y="87.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="33.0" x2="666" y2="33.0"/><text class="dim" x="38" y="36.5" font-size="10.5" text-anchor="end">350</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="54.0" y1="200" x2="54.0" y2="204"/><text class="dim" x="54.0" y="216" font-size="10.5" text-anchor="middle">1 Tem</text><line class="line" x1="194.5" y1="200" x2="194.5" y2="204"/><text class="dim" x="194.5" y="216" font-size="10.5" text-anchor="middle">8 Tem</text><line class="line" x1="334.9" y1="200" x2="334.9" y2="204"/><text class="dim" x="334.9" y="216" font-size="10.5" text-anchor="middle">15 Tem</text><line class="line" x1="475.4" y1="200" x2="475.4" y2="204"/><text class="dim" x="475.4" y="216" font-size="10.5" text-anchor="middle">22 Tem</text><line class="line" x1="615.8" y1="200" x2="615.8" y2="204"/><text class="dim" x="615.8" y="216" font-size="10.5" text-anchor="middle">29 Tem</text><polyline class="curve" points="54.0,182.0 74.1,170.9 94.2,162.7 114.2,131.3 134.3,81.7 154.4,37.1 174.4,75.6 194.5,169.8 214.5,168.8 234.6,157.7 254.7,119.2 274.7,100.9 294.8,39.1 314.9,71.5"/><polyline class="curve" points="395.1,131.3 415.2,91.8 435.3,40.1 455.3,79.6 475.4,152.6 495.5,152.6 515.5,152.6 535.6,132.3 555.6,66.5 575.7,32.0 595.8,80.6 615.8,152.6 635.9,133.4 656.0,145.5"/><circle class="dot" cx="54.0" cy="182.0" r="3.2"/><circle class="dot" cx="74.1" cy="170.9" r="3.2"/><circle class="dot" cx="94.2" cy="162.7" r="3.2"/><circle class="dot" cx="114.2" cy="131.3" r="3.2"/><circle class="dot" cx="134.3" cy="81.7" r="3.2"/><circle class="dot" cx="154.4" cy="37.1" r="3.2"/><circle class="dot" cx="174.4" cy="75.6" r="3.2"/><circle class="dot" cx="194.5" cy="169.8" r="3.2"/><circle class="dot" cx="214.5" cy="168.8" r="3.2"/><circle class="dot" cx="234.6" cy="157.7" r="3.2"/><circle class="dot" cx="254.7" cy="119.2" r="3.2"/><circle class="dot" cx="274.7" cy="100.9" r="3.2"/><circle class="dot" cx="294.8" cy="39.1" r="3.2"/><circle class="dot" cx="314.9" cy="71.5" r="3.2"/><circle class="dot" cx="395.1" cy="131.3" r="3.2"/><circle class="dot" cx="415.2" cy="91.8" r="3.2"/><circle class="dot" cx="435.3" cy="40.1" r="3.2"/><circle class="dot" cx="455.3" cy="79.6" r="3.2"/><circle class="dot" cx="475.4" cy="152.6" r="3.2"/><circle class="dot" cx="495.5" cy="152.6" r="3.2"/><circle class="dot" cx="515.5" cy="152.6" r="3.2"/><circle class="dot" cx="535.6" cy="132.3" r="3.2"/><circle class="dot" cx="555.6" cy="66.5" r="3.2"/><circle class="dot" cx="575.7" cy="32.0" r="3.2"/><circle class="dot" cx="595.8" cy="80.6" r="3.2"/><circle class="dot" cx="615.8" cy="152.6" r="3.2"/><circle class="dot" cx="635.9" cy="133.4" r="3.2"/><circle class="dot" cx="656.0" cy="145.5" r="3.2"/><text class="ink" x="355.0" y="18.5" font-size="11" text-anchor="middle">15–17 Temmuz: kayıt yok</text></svg>
  <figcaption>Temmuz 2024, <code>asfreq("D")</code> sonrası. Üç gün için satır var ama değer boş; çizgi orada kopuyor. Eksiklik artık hem tabloda hem grafikte görünüyor.</figcaption>
</figure>

Artık eksiklik **görünür**: her gün için bir satır var ve boş olanlar belli.
İki not:

- Sütun ondalıklı sayıya döndü (`312.0`), çünkü `NaN` tam sayı sütununda
  duramıyor.
- Boşlukları **şimdi doldurmuyoruz.** Neyle doldurulacağı (önceki değer, ara
  değer, sıfır) ayrı bir karar ve Bölüm 13'ün konusu. Yalnızca "kayıt yoksa
  satış da yok" diyebiliyorsan `asfreq("D", fill_value=0)`.

Tekrarlanan tarih varken `asfreq` çalışmıyor
(`cannot reindex on an axis with duplicate labels`); sıra bu yüzden önemli:
**sırala, tekrarları çöz, sonra takvime oturt.**

## `date_range`: takvim üretmek

Az önce tam takvimi `date_range` ile ürettik. Üç bilgiden ikisini veriyorsun:
başlangıç, bitiş, adet.

```python
pd.date_range("2024-03-01", periods=3, freq="D")      # 1, 2, 3 Mart
pd.date_range("2024-01-01", "2024-06-30", freq="ME")  # ay sonlari: 31 Oca ... 30 Haz
pd.date_range("2024-01-01", periods=3, freq="MS")     # ay baslari: 1 Oca, 1 Sub, 1 Mar
pd.date_range("2024-03-09 08:00", periods=4, freq="6h")   # 08:00, 14:00, 20:00, 02:00
pd.date_range("2024-03-04", "2024-03-17", freq="B")   # is gunleri: 10 gun
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>D</code></span><span>Gün</span></div>
    <div class="anat-row"><span><code>h</code> · <code>min</code> · <code>s</code></span><span>Saat, dakika, saniye (küçük harf)</span></div>
    <div class="anat-row"><span><code>B</code></span><span>İş günü: pazartesi–cuma</span></div>
    <div class="anat-row"><span><code>W</code> · <code>W-MON</code></span><span>Hafta (pazar biten) · pazartesi biten hafta</span></div>
    <div class="anat-row"><span><code>ME</code> · <code>MS</code></span><span>Ay sonu · ay başı</span></div>
    <div class="anat-row"><span><code>QE</code> · <code>YE</code></span><span>Çeyrek sonu · yıl sonu</span></div>
  </div>
  <figcaption>Başına sayı yazılabiliyor: <code>15min</code>, <code>6h</code>, <code>2W</code>. Tam liste "Frekans Kısaltmaları" notunda.</figcaption>
</figure>

**Eski kaynaklarda `freq="M"` ve `"H"` görürsün; artık çalışmıyor.** Yeni
pandas'ta ay sonu `"ME"`, saat küçük harfle `"h"`. `"M"` yazarsan
`Invalid frequency: M` hatası alıyorsun.

## Saatlik veride saatle seçmek

İndekste saat de varsa seçim aynı mantıkla derinleşiyor. Saatlik elektrik
tüketimi (`energy_hourly.csv`):

```python
load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)["load_mw"]

print(len(load.loc["2024-03-15"]))                              # 24   o gunun tamami
print(len(load.loc["2024-03-15 08:00":"2024-03-15 12:00"]))     # 5    saat araligi
```

Tarihten bağımsız olarak **günün saatine göre** seçmek için iki yardımcı var:

```python
day = load.between_time("08:00", "18:00")
night = load.between_time("22:00", "06:00")

print(round(day.mean(), 1), round(night.mean(), 1))   # 1038.1 768.4
print(len(load.at_time("18:00")))                     # 61   her gunun 18:00'i
```

`between_time` gece yarısını geçen aralığı da anlıyor (`22:00`–`06:00`).
Gündüz tüketimi gecenin 1.35 katı: günün saatine bağlı bir mevsimsellik.

## Hizalama: pandas tarihe göre eşleştirir

İki seriyi topladığında pandas satır sırasına değil **indekse** bakıyor:

```python
a = s.loc["2024-01"]                        # 31 gun
b = s.loc["2024-01-15":"2024-02-15"]        # 32 gun

total = a + b
print(len(total), total.notna().sum(), total.isna().sum())   # 46 17 29
```

Sonuç iki aralığın birleşimi kadar uzun (46 gün). İkisinde de olan 17 günde
toplam var; yalnızca birinde olan 29 günde `NaN`. **Aynı tarihler eşleşti,
eşi olmayanlar boş kaldı.** Bu güvenli bir davranış: iki seriyi konumla
toplasaydın 1 Ocak ile 15 Ocak sessizce toplanırdı.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Tarihi indekse almadan `loc["2024-03"]` | `KeyError` | `set_index("date")` |
| `sort_index()` çağırmamak | Dilimlemede `KeyError` | İndeksten hemen sonra sırala |
| `iloc` gibi "son hariç" sanmak | Bir gün fazla | Tarih dilimi iki ucu da alıyor |
| Tekrarları rastgele atmak | Günün değeri eksik | Verinin anlamına göre topla / sonuncuyu al |
| Eksik günleri aramamak | "Önceki satır" dün değil | `date_range` + `difference`, sonra `asfreq` |
| `freq="M"`, `"H"` | `Invalid frequency` | `"ME"`, `"h"` |
| `asfreq` sonrası hemen `fillna(0)` | Olmayan günler "satış yok" sayılıyor | Önce eksikliğin anlamına karar ver |

## Özet

- Tarihi **indekse** al (`set_index` ya da `index_col=..., parse_dates=True`)
  ve hemen **`sort_index()`** çağır.
- Tarihle seç: `loc["2024-03-09"]`, `loc["2024-03"]`, `loc["2024"]`. Dilim
  **iki ucu da** dahil ediyor.
- İndeksin parçaları `.dt` olmadan: `s.index.month`, `s.index.dayofweek`.
- Üç kontrol: `is_monotonic_increasing` (sıralı mı), `is_unique` (tekrar var
  mı), `date_range(...).difference(index)` (eksik var mı).
- Tekrarları verinin anlamına göre çöz (`groupby(level=0)`), sonra
  **`asfreq`** ile tam takvime oturt; eksikler `NaN` olarak görünür olsun.
- `date_range` takvim üretir. Kısaltmalar: `D`, `h`, `min`, `B`, `W`, `ME`,
  `MS`, `QE`, `YE`.
- Saatlik veride `between_time` ve `at_time`. İki seri toplandığında pandas
  tarihe göre hizalıyor.
