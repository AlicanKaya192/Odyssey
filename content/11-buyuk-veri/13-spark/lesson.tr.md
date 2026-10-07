# Spark'ın Mantığı

Geçen bölümün sonunda MapReduce'un iki sınırını gördük: her adım diske
yazıyor ve her şeyi map ile reduce'a çevirmek zahmetli. **Apache Spark** bu
iki soruna cevap olarak doğdu (2009'da Berkeley'de başladı, sonra Apache'ye
geçti). Bugün kümelerde büyük veri işlemenin en yaygın aracı.

Spark'ın iki büyük fikri var:

1. **Ara sonuçları bellekte tutmak.** Veriyi defalarca dolaşan işler (makine
   öğrenmesi gibi) her turda diske gidip gelmiyor.
2. **Zengin ve tembel bir dil.** `map` ve `reduce`'tan çok daha fazla işlem
   var; hepsi önce bir plan olarak kaydediliyor, iş ancak sonuç istenince
   başlıyor.

## Gerçek Spark ve bu bölüm

Gerçek Spark bir küme üstünde çalışıyor ve **Java** istiyor. Python'dan
kullanmak için `pyspark` paketi var; kurulumu için önce bilgisayara Java
(JDK) kurmak gerekiyor. Odyssey'in alıştırmaları kişinin bilgisayarına bir
şey kurmadan çalışsın diye bu bölümde **`minispark`** adlı küçük bir benzetici
kullanıyoruz: alıştırmalarda salt okunur bir sekme olarak duruyor.

`minispark` tek bir Python sürecinde çalışıyor ama Spark'ın **adlarını ve
fikirlerini** birebir taşıyor: bölümler, tembel dönüşümler, eylemler, soy ağacı
(*lineage*), önbellek, shuffle, DataFrame ve SQL. Burada yazdığın kod, birkaç
küçük farkla gerçek PySpark'ta da çalışır.

## Başlamak: SparkSession

```python
from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext
```

- `SparkSession`: Spark'a giriş kapısı. Gerçek Spark'ta küme bağlantısını da
  bu kuruyor.
- `sparkContext` (kısaca `sc`): düşük düzeydeki RDD dünyasının kapısı.

## RDD: bölümlere ayrılmış bir koleksiyon

Spark'ın temel yapısı **RDD** (*Resilient Distributed Dataset*, dayanıklı
dağıtık veri kümesi): bölümlere ayrılmış, değiştirilemez bir öğe
koleksiyonu.

```python
nums = sc.parallelize(range(10), 3)
print(nums.getNumPartitions())
print(nums.glom().collect())
```

```text
3
[[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]
```

`parallelize` bir Python koleksiyonunu üç bölüme dağıttı. `glom` her bölümü
bir liste yapıyor; böylece bölümlerin içini görebiliyoruz. Gerçek kümede her
bölüm başka bir makinede durabilir.

## Dönüşümler ve eylemler

Spark'taki işlemler iki türlü:

<figure class="fig">
  <div class="versus">
    <div><h4>Dönüşüm (tembel)</h4><p><code>map</code>, <code>filter</code>, <code>flatMap</code><br><code>reduceByKey</code>, <code>distinct</code><br>Yeni bir RDD tarif eder<br>Hiçbir şey hesaplamaz</p></div>
    <div class="ok"><h4>Eylem</h4><p><code>collect</code>, <code>count</code>, <code>take</code><br><code>sum</code>, <code>reduce</code><br>Bir sonuç ister<br>Bütün tarifi çalıştırır</p></div>
  </div>
  <figcaption>Dönüşümler zincir gibi eklenir; iş ancak bir eylem gelince başlar.</figcaption>
</figure>

- **Dönüşümler** (*transformations*) yeni bir RDD tarif ediyor ama
  **hiçbir şey hesaplamıyor**: `map`, `filter`, `flatMap`, `reduceByKey`,
  `distinct`…
- **Eylemler** (*actions*) bir sonuç istiyor ve bütün tarifin çalışmasını
  tetikliyor: `collect`, `count`, `take`, `sum`, `reduce`…

`minispark`'ın `sc.stats` sayacıyla bunu görebiliriz. Bölüm 12'deki kelime
sayma, Spark'ta:

```python
lines = sc.parallelize(["the cat sat", "the dog sat", "the cat ran"], 2)
counts = (lines.flatMap(lambda line: line.split())
               .map(lambda word: (word, 1))
               .reduceByKey(lambda a, b: a + b))
print(sc.stats.jobs, sc.stats.partitions_computed)
print(sorted(counts.collect()))
print(sc.stats.jobs, sc.stats.partitions_computed, sc.stats.shuffles)
```

```text
0 0
[('cat', 2), ('dog', 1), ('ran', 1), ('sat', 2), ('the', 3)]
1 8 1
```

- Üç dönüşümden sonra iş sayısı da hesaplanan bölüm sayısı da **0**:
  Spark yalnızca tarif yazdı.
- `collect()` bir eylem: tarif çalıştı. 1 iş, 8 bölüm hesabı (dört adım × iki
  bölüm) ve 1 shuffle.

Bölüm 12'de üç ayrı adım olarak yazdığımız map, shuffle ve reduce burada
üç satır: `flatMap` + `map` map adımı, `reduceByKey` shuffle ile reduce'un
ikisi birden. `reduceByKey` birleştiriciyi de kendisi uyguluyor: her bölümde
önce yerel toplam, sonra shuffle.

## Soy ağacı (lineage) ve dayanıklılık

Her RDD nereden geldiğini, yani kendisini üreten adımları biliyor:

```python
print(counts.toDebugString())
```

```text
+- reduceByKey (shuffle)
  +- map
    +- flatMap
      +- parallelize
```

Bu soy ağacı Spark'ın dayanıklılığının (adındaki *Resilient*) sırrı. Bir
makine bozulup bir bölüm kaybolursa Spark veriyi yedekten okumuyor; o
bölümü soy ağacındaki adımları **yeniden çalıştırarak** baştan hesaplıyor.
Dönüşümler yan etkisiz olduğu için aynı sonuç çıkıyor.

## Dar ve geniş dönüşümler

Soy ağacındaki `(shuffle)` işaretine dikkat:

- **Dar dönüşüm** (*narrow*): her bölüm yalnızca kendi verisiyle
  hesaplanıyor. `map`, `filter`, `flatMap`. Makineler arası veri gitmiyor;
  ucuz.
- **Geniş dönüşüm** (*wide*): bir bölümün sonucu birçok bölümün verisine
  bağlı. `reduceByKey`, `groupByKey`, `distinct`, `sortBy`. Bir **shuffle**
  gerekiyor: veri ağdan makineler arasında yer değiştiriyor; pahalı.

Spark bir işi shuffle'lardan **aşamalara** (*stages*) bölüyor; bir aşamanın
içindeki dar dönüşümler veriyi bellekte, art arda geçiriyor. İyi bir Spark
kodu shuffle sayısını az tutuyor. Örneğin `groupByKey` her değeri ağdan
taşırken `reduceByKey` önce bölüm içinde birleştirdiği için çok daha az veri
gönderiyor (Bölüm 12'deki birleştirici).

## Önbellek: aynı veriyi iki kez hesaplamamak

Bir RDD'yi iki eylemde kullanırsan, Spark tembel olduğu için tarifi **iki
kez** çalıştırıyor. `cache()` ilk hesaplanışta sonucu bellekte tutmasını
söylüyor:

```python
squares = nums.map(lambda x: x * x).cache()
before = sc.stats.partitions_computed
squares.count()
squares.sum()
print(sc.stats.partitions_computed - before)
```

```text
6
```

İki eylem toplam 6 bölüm hesabı yaptı: `count` iki adımın üç bölümünü
hesapladı, `sum` önbellekten okudu. `cache()` olmasaydı `sum` hepsini yeniden
hesaplayacaktı: 12. Spark'ın makine öğrenmesinde MapReduce'tan kat kat
hızlı olmasının sebebi bu: veriyi defalarca dolaşan algoritma her turda
önbellekten okuyor.

## DataFrame: tablolar ve plan

RDD'ler esnek ama alçak düzeyde. Günlük işte Spark'ın **DataFrame**'i
kullanılıyor: pandas'taki gibi sütunlu bir tablo, ama bölümlere ayrılmış ve
tembel.

```python
from orders_data import make_orders

df = spark.createDataFrame(make_orders(100_000), numPartitions=4)
big = df.withColumn("revenue", "quantity * unit_price").filter("quantity >= 4")
summary = big.groupBy("city").agg({"revenue": "sum", "order_id": "count"}).orderBy("city")
summary.show()
```

```text
    city  sum(revenue)  count(order_id)
   Adana    4784431.21             1518
  Ankara   11477315.59             3587
 Antalya    6671726.14             2064
   Bursa    6461439.90             1997
Istanbul   24791508.41             7554
   Izmir    9588024.17             2873
   Konya    5142625.90             1538
 Trabzon    3496253.54             1045
```

- `withColumn` yeni sütun, `filter` süzme, `groupBy(...).agg(...)` gruplama:
  hepsi dönüşüm, hepsi tembel.
- `show()` bir eylem: plan şimdi çalıştı.

(Gerçek PySpark'ta koşullar çoğu zaman sütun nesneleriyle yazılıyor:
`df.filter(df.quantity >= 4)`. `minispark` metin olarak alıyor.)

Planı görmek için `explain()`:

```python
summary.explain()
```

```text
+- orderBy(city) (shuffle)
  +- groupBy(city).agg({'revenue': 'sum', 'order_id': 'count'}) (shuffle)
    +- filter(quantity >= 4)
      +- withColumn(revenue = quantity * unit_price)
        +- createDataFrame(4 partitions)
```

Gerçek Spark planı çalıştırmadan önce **iyileştiriyor** (Catalyst adlı bir
iyileştirici): süzmeyi okumanın hemen yanına taşıyor, yalnızca gereken
sütunları okuyor, birleştirmeleri yeniden sıralıyor. Parquet'deki sütun
seçme ve istatistikle atlama (Bölüm 5) Spark'ta da kendiliğinden yapılıyor.

## Spark SQL

Bir DataFrame'i ad verip SQL ile de sorgulayabilirsin:

```python
df.createOrReplaceTempView("orders")
spark.sql("""
    SELECT payment, count(*) AS n
    FROM orders
    GROUP BY payment
    ORDER BY n DESC
""").show()
```

```text
 payment     n
    card 72243
transfer 19885
    cash  7872
```

DataFrame yazımı ile SQL aynı plana dönüşüyor; hangisini daha okunur
buluyorsan onu yaz. (`minispark` SQL'i arkada DuckDB ile çalıştırıyor;
gerçek Spark'ın kendi SQL motoru var.)

## Kümede Spark

<figure class="fig">
  <div class="flow">
    <span class="node acc">Sürücü<br>plan, görevler</span><span class="arrow">→</span>
    <span class="node">Küme yöneticisi<br>makine, bellek</span><span class="arrow">→</span>
    <span class="node">Yürütücüler<br>bölümleri işler</span>
  </div>
  <figcaption>Sürücü senin programın; yürütücüler kümedeki makinelerde bölümleri işliyor ve önbelleği tutuyor.</figcaption>
</figure>

- **Sürücü** (*driver*): senin programın; planı kuruyor, görevleri
  dağıtıyor, sonuçları topluyor.
- **Yürütücüler** (*executors*): kümedeki makinelerde çalışan işçiler; her
  biri bölümleri işliyor ve önbelleği tutuyor.
- **Küme yöneticisi**: makineleri ve belleği işlere dağıtıyor (YARN,
  Kubernetes ya da Spark'ın kendi yöneticisi).

`collect()` bütün sonucu sürücüye getiriyor; sonuç büyükse sürücünün belleği
dolar. Büyük sonuç diske yazılır (`df.write.parquet(...)`), sürücüye
getirilmez. Bu, Bölüm 8'deki "büyük sonucu pandas'a alma" kuralının kümedeki
karşılığı.

## Spark, dask, DuckDB: hangisi?

| Durum | Uygun araç |
|---|---|
| Tek makine, dosyada SQL | DuckDB |
| Tek makine, pandas yazımı, bellekten büyük | dask |
| Birçok makine, terabaytlar, kurumsal küme | Spark |
| Birçok makine, Python ağırlıklı iş | dask (dağıtık) ya da Spark |

Çoğu analiz için tek bir güçlü makine ve doğru araç (Parquet + DuckDB)
yeterli. Spark, veri gerçekten tek makineyi aştığında ve bir küme zaten
olduğunda öne çıkıyor.

## Özet

- Spark ara sonuçları bellekte tutuyor ve zengin, tembel bir dil sunuyor;
  MapReduce'un iki sınırına cevap.
- RDD: bölümlere ayrılmış, değiştirilemez koleksiyon. Dönüşümler tembel,
  eylemler çalıştırıyor.
- Soy ağacı: kaybolan bölüm adımlar yeniden çalıştırılarak hesaplanıyor.
- Dar dönüşüm bölüm içinde, geniş dönüşüm shuffle ister; `reduceByKey`
  `groupByKey`'den ucuz.
- `cache()` aynı RDD'nin iki kez hesaplanmasını önlüyor (bu örnekte 12 yerine
  6 bölüm hesabı).
- DataFrame ve Spark SQL aynı plana dönüşüyor; `explain()` planı gösteriyor.
- Kümede sürücü ve yürütücüler; `collect()` sonucu sürücüye getiriyor, büyük
  sonuç diske yazılır.
