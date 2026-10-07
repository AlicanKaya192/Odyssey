# MapReduce

Şimdiye kadarki her şey **tek bir bilgisayarda** oldu: daha akıllı türler,
parça parça okuma, çekirdekler. Peki veri yüzlerce terabayt ise ve hiçbir
tek makinenin diskine bile sığmıyorsa? Bölüm 0'daki yatay ölçekleme:
**birçok makine**.

Birçok makineyle çalışmanın zor yanı makinelerin kendisi değil, işi onlara
bölmek: hangi makine hangi veriyi işleyecek, sonuçlar nasıl birleşecek, bir
makine bozulursa ne olacak? Google 2004'te bu sorulara basit bir cevap
yayımladı: **MapReduce**. Programcı yalnızca iki küçük fonksiyon yazıyor;
gerisini sistem hallediyor. Hadoop bu fikrin herkesin kullanabildiği açık
kaynak uygulaması oldu ve büyük veri sözünün yayılmasını sağladı.

Bu bölümde MapReduce'u saf Python'la, adım adım kendimiz kuracağız. Amaç bir
küme kurmak değil; bir küme üstünde çalışan her aracın (Hadoop, Spark, dask)
arkasındaki düşünceyi anlamak.

## Önce depolama: HDFS

Hadoop'un dosya sistemi **HDFS** büyük bir dosyayı **bloklara** bölüyor
(varsayılan blok 128 MB) ve her bloğu farklı makinelere **üç kopya** olarak
yazıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Blok 1 (128 MB)</span><span>Makine A · Makine C · Makine E</span></div>
    <div class="anat-row"><span>Blok 2 (128 MB)</span><span>Makine B · Makine D · Makine A</span></div>
    <div class="anat-row"><span>Blok 3 (128 MB)</span><span>Makine C · Makine E · Makine B</span></div>
    <div class="anat-row"><span>…</span><span>her blok üç ayrı makinede</span></div>
  </div>
  <figcaption>Büyük bir dosya HDFS'te bloklara bölünüp kopyalanıyor. Bir makine bozulsa da her bloğun iki kopyası kalıyor.</figcaption>
</figure>

Bundan iki şey çıkıyor:

1. **Makine bozulması felaket değil.** Bir bloğun bir kopyası gitse bile iki
   kopyası başka makinelerde duruyor.
2. **Kodu veriye götür.** 1 TB veriyi ağdan tek bir makineye taşımak
   saatler sürer; birkaç kilobaytlık programı verinin olduğu makinelere
   göndermek saniyeler. MapReduce her parçayı, o parçanın durduğu makinede
   işliyor.

## Üç adım: map, shuffle, reduce

<figure class="fig">
  <div class="flow">
    <span class="node">Bloklar</span><span class="arrow">→</span>
    <span class="node">Map<br>(anahtar, değer)</span><span class="arrow">→</span>
    <span class="node">Shuffle<br>grupla</span><span class="arrow">→</span>
    <span class="node">Reduce<br>birleştir</span><span class="arrow">→</span>
    <span class="node acc">Sonuç</span>
  </div>
  <figcaption>Map ve reduce'u programcı yazıyor; shuffle'ı, dağıtmayı ve bozulan makineyi sistem hallediyor.</figcaption>
</figure>

1. **Map (eşle):** her kayıt için bir ya da birkaç **(anahtar, değer)**
   çifti üret. Her makine kendi bloğundaki kayıtlar için bunu yapıyor.
2. **Shuffle (karıştır, dağıt):** aynı anahtara sahip bütün çiftleri, hangi
   makineden gelirse gelsin, **aynı yere** topla.
3. **Reduce (indir):** her anahtarın değer listesinden tek bir sonuç çıkar.

Programcı yalnızca `map` ve `reduce` fonksiyonlarını yazıyor. Shuffle'ı,
makinelere dağıtmayı ve bozulan makineyi sistem yapıyor.

## Klasik örnek: kelime sayma

Üç satırlık bir metinde her kelimenin kaç kez geçtiği:

```python
from collections import defaultdict

text = ["the cat sat", "the dog sat", "the cat ran"]

def mapper(line):
    for word in line.split():
        yield word, 1

pairs = [pair for line in text for pair in mapper(line)]
print(pairs[:4])
print(len(pairs))
```

```text
[('the', 1), ('cat', 1), ('sat', 1), ('the', 1)]
9
```

`mapper` bir satır alıp her kelime için `(kelime, 1)` çifti üretiyor.
`yield` bir fonksiyonun değerleri tek tek **üretmesini** sağlıyor (bu
fonksiyon bir üreteç); liste kurup döndürmeye gerek kalmıyor.

Shuffle: aynı kelimenin bütün değerlerini bir listede topla.

```python
groups = defaultdict(list)
for key, value in pairs:
    groups[key].append(value)
print(dict(groups))
```

```text
{'the': [1, 1, 1], 'cat': [1, 1], 'sat': [1, 1], 'dog': [1], 'ran': [1]}
```

`defaultdict(list)`: olmayan bir anahtara ilk kez erişince kendiliğinden boş
bir liste açan sözlük.

Reduce: her kelimenin listesini topla.

```python
def reducer(key, values):
    return key, sum(values)

print(sorted(reducer(k, v) for k, v in groups.items()))
```

```text
[('cat', 2), ('dog', 1), ('ran', 1), ('sat', 2), ('the', 3)]
```

Üç satırda üç adım. Aynı üç fonksiyon üç satıra da üç milyar satıra da
uygulanabiliyor; fark yalnızca kaç makinenin çalıştığı.

## Siparişlerde MapReduce

Bölüm 3'ten beri bildiğimiz şehir başına ciroyu MapReduce ile hesaplayalım.
Her sipariş bir kayıt:

```python
rows = orders[["city", "quantity", "unit_price"]].to_dict("records")

def mapper(row):
    yield row["city"], row["quantity"] * row["unit_price"]

def reducer(key, values):
    return key, sum(values)

groups = defaultdict(list)
for row in rows:
    for key, value in mapper(row):
        groups[key].append(value)
result = dict(reducer(k, v) for k, v in groups.items())
```

İstanbul 557,00, Ankara 260,83, İzmir 212,50 milyon: Bölüm 3'teki, 7'deki
ve 11'deki sonuçların aynısı.

Tek makinede bu yol yavaş: bir milyon siparişte 0,49 saniye, pandas'ın
`groupby`'ı 0,058 saniye. MapReduce'un değeri tek makinede hız değil;
aynı kodun **yüzlerce makineye** bölünebilmesi.

## Birleştirici (combiner): ağı korumak

Shuffle adımında çiftler makineler arasında **ağdan** taşınıyor ve ağ,
kümenin en yavaş parçası. Bir milyon siparişi dört makineye böldüğümüzü
düşünelim. Her makine her sipariş için bir çift gönderirse ağdan bir milyon
çift geçer.

Ama her makine, göndermeden önce **kendi çiftlerini** şehir başına
toplayabilir. Buna **birleştirici** (*combiner*) deniyor:

```python
chunks = [orders.iloc[i * 250_000:(i + 1) * 250_000] for i in range(4)]
without = 0
with_combiner = 0
for chunk in chunks:
    pairs = list(zip(chunk["city"], chunk["quantity"] * chunk["unit_price"]))
    without += len(pairs)
    local = defaultdict(float)
    for key, value in pairs:
        local[key] += value
    with_combiner += len(local)
print(without, with_combiner)
```

```text
1000000 32
```

Bir milyon çift yerine 32 çift (4 makine × 8 şehir). Bölüm 3'teki "parçada
özetle, özetleri birleştir" kalıbının dağıtık hâli. Ve aynı sınır geçerli:
toplam ve sayı birleştiriciyle olur, ortanca olmaz.

## Anahtarı makineye dağıtmak

Shuffle'da "aynı anahtar aynı yere" kuralını sağlamak için her anahtara bir
**reduce makinesi** seçmek gerekiyor. Yaygın yol: anahtarın **karma
değerini** (*hash*) makine sayısına bölüp kalana bakmak.

Python'un `hash()` fonksiyonu akla gelen ilk araç, ama bir tuzağı var. Aynı
satırı beş ayrı Python sürecinde çalıştırdım:

```python
print(hash("Istanbul") % 4)
```

```text
2
1
0
2
1
```

Beş süreç, beş farklı cevap. Python güvenlik için metin karmasını her süreçte
rastgele bir tohumla hesaplıyor. Farklı makineler "İstanbul nereye gidecek?"
sorusuna farklı cevap verirse İstanbul'un değerleri dağılır ve sonuç bozulur.
Çözüm, her yerde aynı sonucu veren **kararlı** bir karma: `zlib.crc32`.

```python
import zlib

def partition(key, reducers):
    return zlib.crc32(key.encode()) % reducers
```

`partition("Istanbul", 4)` her süreçte, her makinede 1.

## Veri çarpıklığı

Sekiz şehri `partition(şehir, 3)` ile üç reduce makinesine dağıtınca:

| Makine | Şehirler | Siparişlerin payı |
|---|---|---|
| 0 | Ankara, Antalya, İstanbul, Konya | %66 |
| 1 | Adana, Bursa, İzmir | %29 |
| 2 | Trabzon | %5 |

0 numaralı makine işin üçte ikisini alıyor; 2 numaralı makine işini çabuk
bitirip bekliyor. Bütün iş **en yavaş makine** bitince bitiyor. Buna **veri
çarpıklığı** (*data skew*) deniyor ve gerçek kümelerde en sık görülen
yavaşlık sebeplerinden biri.

Çareler:

- **Daha çok reduce makinesi:** büyük anahtar yine tek makinede kalır ama
  diğerleri dağılır.
- **Anahtarı tuzlamak** (*salting*): çok büyük bir anahtarı parçalara bölmek,
  örneğin `Istanbul#0`, `Istanbul#1`, `Istanbul#2`; sonra parça sonuçlarını
  ikinci bir küçük adımda birleştirmek.

## Sıralayarak gruplamak

Gerçek MapReduce sistemleri shuffle'da çiftleri **anahtara göre sıralıyor**;
reduce adımı sıralı listeyi baştan sona bir kez geçerek her anahtarın
değerlerini topluyor. Python'daki karşılığı `itertools.groupby`:

```python
from itertools import groupby

pairs = [("b", 1), ("a", 1), ("b", 1), ("c", 1), ("a", 1)]
pairs.sort()
for key, group in groupby(pairs, key=lambda kv: kv[0]):
    print(key, sum(v for _, v in group))
```

```text
a 2
b 2
c 1
```

`groupby` yalnızca **yan yana** duran aynı anahtarları birleştiriyor; liste
sıralı değilse aynı anahtar birden çok grup olarak gelir. Bu yüzden önce
`sort()`. Sıralı liste bellekte bütün grupları tutmadan, akarak işleniyor;
büyük veride sözlükte biriktirmekten daha az bellek istiyor.

## Bozulan makine

Yüzlerce makinede biri mutlaka bozuluyor. MapReduce'ta bu kolay: her map
görevi yalnızca kendi bloğunu okuyor ve sonucu başka hiçbir şeyi
değiştirmiyor. Bir makine giderse yönetici o görevi bloğun **başka bir
kopyasının** durduğu makinede yeniden çalıştırıyor. Görevlerin yan etkisiz
olması ("aynı girdiye her seferinde aynı çıktı") bunu mümkün kılıyor.

## MapReduce'un sınırları

- Her adımın sonucu **diske** yazılıyor. Tek geçişlik işler için sağlam, ama
  veriyi defalarca dolaşan işler (makine öğrenmesi algoritmaları, grafik
  hesapları) her turda diske yazıp okuduğu için çok yavaş.
- Her şeyi map ve reduce'a çevirmek zahmetli: birleştirme (JOIN) gibi işler
  birkaç MapReduce adımı gerektiriyor.

Bu iki sınır bir sonraki bölümün konusunu doğurdu: ara sonuçları **bellekte**
tutan ve SQL'e benzer bir dil sunan **Spark**.

## Özet

- Veri tek makineye sığmayınca birçok makine; HDFS dosyayı 128 MB'lık
  bloklara bölüp her bloğu üç kopya saklıyor; kod verinin olduğu makineye
  gidiyor.
- MapReduce: **map** (kayıt → anahtar–değer çiftleri), **shuffle** (aynı
  anahtar aynı yere), **reduce** (anahtarın değerleri → tek sonuç).
- Birleştirici her makinede önceden topluyor: bir milyon çift yerine 32.
- Anahtarı makineye dağıtmak için kararlı karma (`zlib.crc32`); Python'un
  `hash()`'i her süreçte farklı.
- Veri çarpıklığı: bir makine işin üçte ikisini alırsa herkes onu bekliyor.
- Her adım diske yazdığı için tekrarlı işlerde yavaş; Spark bu yüzden
  doğdu.
