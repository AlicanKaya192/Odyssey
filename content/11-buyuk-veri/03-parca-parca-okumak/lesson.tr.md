# Parça Parça Okumak

Doğru türlerle tablo dört kat küçüldü. Peki dosya 200 GB ise? Dört kat
küçülse bile 50 GB; çoğu bilgisayara yine sığmaz.

Uzun bir kitabı okurken bütün sayfaları aynı anda masana yaymıyorsun. Bir
sayfayı okuyor, aklında kalması gerekeni not alıyor, sayfayı çeviriyorsun.
Masada her an tek bir sayfa ve küçük bir not defteri var.

Bu bölümde dosyayı aynı şekilde okuyacağız: **parça parça**. Bellekte her
an yalnızca bir parça ve küçük bir ara sonuç duracak. İngilizcede buna
*out-of-core* (bellek dışı) işleme deniyor: verinin tamamı hiçbir zaman
belleğe girmiyor.

Bölümdeki örnekler bir milyon siparişlik dosyayla çalışıyor:

```python
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
```

## Önce bir göz at: `nrows`

Büyük bir dosyayla karşılaşınca ilk iş onu baştan sona okumak değil, ilk
birkaç satırına bakmak. `nrows` yalnızca o kadar satırı okuyor:

```python
print(pd.read_csv("orders.csv", nrows=3).to_string(index=False))
```

```text
 order_id          order_time  customer_id     city category  quantity  unit_price  payment
        1 2024-01-01 00:00:47        45209 Istanbul     toys         2      207.09 transfer
        2 2024-01-01 00:01:01        86038  Trabzon clothing         1      437.73     card
        3 2024-01-01 00:02:18        64622    Konya clothing         2      283.38     card
```

Sütun adları, değerlerin biçimi, tarihin nasıl yazıldığı: dosyanın tamamını
okumadan türlere ve sütunlara karar verebilirsin.

## `chunksize`: dosyayı parçalara böl

`read_csv`'ye `chunksize=` verince tablo dönmüyor; **bir okuyucu** dönüyor.
Okuyucuyu bir `for` döngüsünde gezince her adımda bir parça geliyor:

```python
reader = pd.read_csv("orders.csv", chunksize=100_000)
print(type(reader).__name__)
for i, chunk in enumerate(reader):
    print(i, len(chunk), chunk["order_id"].iloc[0], chunk["order_id"].iloc[-1])
```

```text
TextFileReader
0 100000 1 100000
1 100000 100001 200000
2 100000 200001 300000
3 100000 300001 400000
4 100000 400001 500000
5 100000 500001 600000
6 100000 600001 700000
7 100000 700001 800000
8 100000 800001 900000
9 100000 900001 1000000
```

- Her `chunk` sıradan bir `DataFrame`; bildiğin her şeyi onunla
  yapabilirsin.
- Bir parça 100 000 satır: bellekte yaklaşık 9,6 MB. Bütün dosya 96 MB.
- Okuyucu bir kez gezilebiliyor; ikinci kez gezmek için `read_csv`'yi
  yeniden çağırman gerekiyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Parçayı oku</span><span class="arrow">→</span>
    <span class="node">Parçada özetle</span><span class="arrow">→</span>
    <span class="node">Not defterine ekle</span><span class="arrow">→</span>
    <span class="node">Parçayı bırak</span><span class="arrow">→</span>
    <span class="node acc">Sonuç</span>
  </div>
  <figcaption>İlk dört adım her parça için tekrar ediyor; parçalar bitince not defterinden sonuç çıkıyor. Bellekte her an bir parça ve küçük bir not defteri var.</figcaption>
</figure>

## Biriktirmek: parçalardan toplam

Bütün siparişlerin cirosunu (adet × fiyat) parçalarla hesaplayalım. Fikir
basit: her parçanın toplamını hesapla, bir değişkende **biriktir**.

```python
total = 0
rows = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    revenue = chunk["quantity"] * chunk["unit_price"]
    total += revenue.sum()
    rows += len(chunk)
print(rows, round(total, 2))
```

```text
1000000 1635737361.77
```

Dosyanın tamamını okuyup hesaplasaydık sonuç birebir aynı olurdu:
1 635 737 361,77. Ama bellekte hiçbir zaman bir parçadan fazlası durmadı.

`total` ve `rows` döngü boyunca taşınan küçük not defteri: her parça bittikten
sonra elimizde yalnızca iki sayı kalıyor.

## Tuzak 1: ortalamaların ortalaması

Ortalama fiyatı parçalarla bulmak isteyelim. İlk akla gelen yol her parçanın
ortalamasını alıp onların ortalamasını almak. Parça büyüklüğünü 300 000
yapalım (son parça 100 000 satır kalacak):

```python
means = []
total = 0
count = 0
for chunk in pd.read_csv("orders.csv", chunksize=300_000):
    means.append(float(chunk["unit_price"].mean()))
    total += chunk["unit_price"].sum()
    count += len(chunk)
print([round(m, 2) for m in means])
print(round(sum(means) / len(means), 4))
print(round(total / count, 4))
```

```text
[737.47, 737.53, 736.77, 733.38]
736.287
736.869
```

İki sonuç farklı. Gerçek ortalama (dosyanın tamamından) 736,869. Ortalamaların
ortalaması yanlış, çünkü 100 000 satırlık son parçaya da 300 000 satırlık
parçalar kadar ağırlık veriyor.

Doğru yol: **toplamı ve sayıyı** ayrı ayrı biriktirip en sonda bölmek.
Ortalama birleştirilemez; ama toplam ve sayı birleştirilebilir.

## Parçalarla gruplamak

Şehir başına ciroyu parçalarla bulalım. Her parçada `groupby` ile şehir
başına toplamı alıp bir listeye koyuyoruz; sonunda parça sonuçlarını
birleştirip bir kez daha topluyoruz:

```python
parts = []
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    chunk["revenue"] = chunk["quantity"] * chunk["unit_price"]
    parts.append(chunk.groupby("city")["revenue"].sum())

combined = pd.concat(parts).groupby(level=0).sum()
print((combined / 1e6).round(2).sort_values(ascending=False))
```

```text
city
Istanbul    557.00
Ankara      260.83
Izmir       212.50
Bursa       147.92
Antalya     146.01
Adana       115.39
Konya       114.42
Trabzon      81.66
Name: revenue, dtype: float64
```

- `parts` 10 küçük seri tutuyor; her biri 8 satır (8 şehir). Bellekte
  neredeyse hiç yer kaplamıyor.
- `pd.concat(parts)` 80 satırlık tek bir seri yapıyor; aynı şehir 10 kez
  geçiyor.
- `groupby(level=0).sum()` indekse (şehir adına) göre bir kez daha
  topluyor.

Bu kalıp iki adımlı: **parçada özetle, sonra özetleri birleştir.** Toplam,
sayı, en küçük ve en büyük değer bu kalıba uyuyor.

## Tuzak 2: farklı değer sayısı

Kaç farklı müşteri var? Her parçanın `nunique()` sonucunu toplamak yanlış:

```python
seen = set()
wrong = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000, usecols=["customer_id"]):
    seen.update(chunk["customer_id"])
    wrong += chunk["customer_id"].nunique()
print(len(seen))
print(wrong)
```

```text
245461
824660
```

Aynı müşteri birçok parçada sipariş vermiş; parça başına sayınca bir kişiyi
birçok kez sayıyorsun. Doğrusu, görülen müşterileri bir kümede (`set`)
toplamak: küme bir değeri bir kez tutuyor. Ama bedeli var: küme her farklı
müşteriyi bellekte saklıyor. Farklı değer sayısı çok büyükse bu da sığmayabilir.

**Ortanca** (median) daha da zor: her parçanın ortancası ile bütünün
ortancası arasında bir ilişki yok. Ortancayı kesin bulmak için bütün
değerler gerekiyor. Yaklaşık sonuç yolları Bölüm 9'da.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Toplam, sayı, en küçük, en büyük</span><span>Doğrudan birleşir: topla ya da en küçüğünü / en büyüğünü al</span></div>
    <div class="anat-row"><span>Ortalama</span><span>Toplamı ve sayıyı biriktir, en sonda böl</span></div>
    <div class="anat-row"><span>Farklı değer sayısı</span><span>Görülen değerleri bir kümede topla</span></div>
    <div class="anat-row"><span>Ortanca, yüzdelikler</span><span>Parçalardan kesin bulunamaz</span></div>
  </div>
  <figcaption>Kontrol sorusu: iki parçanın sonucunu bilsem, ikisinin birleşiminin sonucunu bulabilir miyim?</figcaption>
</figure>

## Süzüp küçük sonucu tutmak

Çoğu zaman bütün dosya gerekmiyor, yalnızca bir kısmı. Her parçayı süzüp
kalanları biriktirebilirsin:

```python
pieces = []
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    pieces.append(chunk[chunk["category"] == "electronics"])
electronics = pd.concat(pieces, ignore_index=True)
print(len(electronics), round(electronics.memory_usage(deep=True).sum() / 1024**2, 1))
```

```text
139775 14.1
```

Bir milyon satırdan 139 775 elektronik siparişi kaldı: 14,1 MB. Sonuç
belleğe sığdığı sürece bu yol işe yarıyor. `ignore_index=True` parçaların
eski indekslerini atıp 0'dan başlayan yeni bir indeks veriyor.

## Sonucu da parça parça yazmak

Süzülen sonuç bile belleğe sığmayacak kadar büyükse onu da biriktirme;
her parçanın sonucunu dosyaya **ekle**:

```python
first = True
for chunk in pd.read_csv("orders.csv", chunksize=250_000):
    big = chunk[chunk["quantity"] >= 4]
    big.to_csv("big_orders.csv", mode="w" if first else "a", header=first, index=False)
    first = False
```

- `mode="w"`: ilk parçada dosyayı sıfırdan yaz.
- `mode="a"`: sonraki parçalarda dosyanın sonuna ekle (*append*).
- `header=first`: sütun adları yalnızca bir kez, en başa.

Bu kalıpla girdi de çıktı da belleğe hiç sığmasa bile iş yapılabiliyor.

## Parçalar belleği ne kadar korur?

Yalnızca iki sayı sütunuyla ciroyu iki yolla hesaplayıp `tracemalloc` ile
tepeye bakalım:

```python
import tracemalloc

columns = ["quantity", "unit_price"]

tracemalloc.start()
total = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000, usecols=columns):
    total += (chunk["quantity"] * chunk["unit_price"]).sum()
print("chunks peak", round(tracemalloc.get_traced_memory()[1] / 1024**2, 1))
tracemalloc.stop()

tracemalloc.start()
df = pd.read_csv("orders.csv", usecols=columns)
total = (df["quantity"] * df["unit_price"]).sum()
print("full peak", round(tracemalloc.get_traced_memory()[1] / 1024**2, 1))
tracemalloc.stop()
```

```text
chunks peak 4.7
full peak 23.8
```

Parçalarla tepe 4,7 MB, tek seferde 23,8 MB. Tek seferde okurken tepe
dosyayla birlikte büyüyor; parçalarla okurken bir parçanın boyutunda kalıyor,
çünkü önceki parça bir sonraki gelmeden bırakılıyor. Parçalarla okumanın asıl
gücü bu: **bellek dosyanın boyutuna bağlı değil, parçanın
boyutuna bağlı.**

(Burada `usecols` ile yalnızca sayı sütunlarını okuduk; `tracemalloc` sayı
sütunlarını görüyor, metin sütunlarını görmüyor.)

## Parça ne büyüklükte olmalı?

Aynı şehir cirosu hesabını farklı parça büyüklükleriyle bu bilgisayarda
ölçtüm:

| Yol | Süre |
|---|---|
| Tek seferde | 0,89 sn |
| 10 000 satırlık parçalar | 1,23 sn |
| 100 000 satırlık parçalar | 0,96 sn |
| 500 000 satırlık parçalar | 0,89 sn |

Çok küçük parça yavaş: her parçada pandas'ın sabit bir hazırlık işi var ve
10 000 satırlık 100 parçada bu iş 100 kez yapılıyor. Parça büyüdükçe süre tek
seferdekine yaklaşıyor. Kural: parça **belleğe rahatça sığacak kadar küçük,
hazırlık işini önemsiz kılacak kadar büyük** olsun. Birkaç on megabaytlık
parçalar çoğu zaman iyi bir başlangıç: bu tabloda 100 000 satır yaklaşık
10 MB.

## pandas olmadan: satır satır okumak

Python dosyayı zaten satır satır okuyabiliyor. Standart kütüphanedeki `csv`
modülüyle her satır bir sözlük olarak geliyor:

```python
import csv

total = 0.0
with open("orders.csv", newline="") as f:
    for row in csv.DictReader(f):
        total += int(row["quantity"]) * float(row["unit_price"])
print(round(total, 2))
```

```text
1635737361.77
```

Sonuç aynı. Bellekte her an tek bir satır var; dosya ne kadar büyük olursa
olsun bellek değişmiyor. Bedeli hız: bu bilgisayarda 1,74 saniye, pandas
parçalarıyla 0,96 saniye. Her değer metinden sayıya tek tek Python'da
çevriliyor (`int(...)`, `float(...)`).

`for row in ...` döngüsünün çalışma biçimi önemli: dosya nesnesi ve
`csv.DictReader` bütün satırları bir listeye koymuyor, her adımda **bir
sonraki** satırı üretiyor. Python'da bu tür nesnelere **yineleyici**
(*iterator*) deniyor. pandas'ın `chunksize` okuyucusu da aynı fikir, yalnızca
satır yerine parça üretiyor.

## Özet

- `nrows=` ile önce birkaç satıra bak.
- `chunksize=` bir okuyucu veriyor; her adımda bir `DataFrame` parçası
  geliyor. Bellek dosyaya değil parçaya bağlı.
- Kalıp: **parçada özetle, özetleri birleştir.** Toplam, sayı, en küçük, en
  büyük doğrudan birleşiyor.
- Ortalamaların ortalaması yanlış: toplam ve sayıyı ayrı biriktir, sonda
  böl.
- Parça başına `nunique()` toplanmaz; `set` ile birleştir. Ortanca
  parçalardan kesin bulunamaz.
- Süzülen sonuç küçükse `pd.concat`, büyükse `to_csv(mode="a")` ile dosyaya
  ekle.
- Parça çok küçükse yavaş; birkaç on megabayt iyi bir başlangıç.
- `csv` modülü ile satır satır okumak her boyutta çalışır ama daha yavaş.
