# DuckDB: Dosyada SQL

SQL patikasında sorguları bir **sunucuya** gönderiyordun: SQL Server ayrı
bir program olarak çalışıyor, veriyi kendi içinde saklıyordu. Bu bölümün
aracı DuckDB ise bambaşka bir fikir: **Python programının içinde çalışan**
bir veritabanı. Kurulacak bir sunucu yok, bağlanılacak bir adres yok; `import
duckdb` yetiyor. Üstelik veriyi önce içine aktarman gerekmiyor: CSV ve
Parquet dosyalarına **doğrudan** SQL yazabiliyorsun.

<figure class="fig">
  <div class="versus">
    <div><h4>SQL Server</h4><p>Ayrı bir program, ayrı kurulum<br>Veriyi önce içine aktarırsın<br>Python ona bir adresten bağlanır<br>Birçok kullanıcı, birçok işlem</p></div>
    <div class="ok"><h4>DuckDB</h4><p>Python'un içinde, <code>import duckdb</code><br>CSV ve Parquet'yi doğrudan sorgular<br>Sunucu yok, adres yok<br>Analiz için: sütun sütun, bütün çekirdekler</p></div>
  </div>
  <figcaption>İkisi de SQL konuşuyor, ama farklı işler için yapıldılar. DuckDB'ye "analiz için SQLite" de deniyor.</figcaption>
</figure>

DuckDB analiz için tasarlandı: veriyi sütun sütun işliyor, bilgisayarın
bütün çekirdeklerini kullanıyor ve tabloyu belleğe tamamen almadan
çalışabiliyor. Bu yüzden büyük dosyalarda pandas'tan çoğu zaman çok daha
hızlı.

Örnekler aynı bir milyon siparişin üç kopyasıyla çalışıyor: `orders.csv`,
`orders.parquet` ve aya göre bölünmüş `orders/` klasörü.

## İlk sorgu

```python
import duckdb

r = duckdb.sql("SELECT count(*) AS orders FROM 'orders.parquet'")
print(r)
print(r.fetchall())
```

```text
┌─────────┐
│ orders  │
│  int64  │
├─────────┤
│ 1000000 │
└─────────┘

[(1000000,)]
```

- `duckdb.sql(...)` sorguyu çalıştırıp bir **sonuç nesnesi** döndürüyor;
  yazdırınca kutulu bir tablo çiziliyor. Her sütunun altında türü yazıyor
  (`int64`).
- `fetchall()` sonucu Python listesi olarak veriyor: her satır bir demet.
- `FROM 'orders.parquet'`: **tek tırnak içindeki dosya adı** tablo adı
  yerine geçiyor. DuckDB uzantıdan biçimi anlıyor; `'orders.csv'` da aynı
  şekilde çalışıyor.

## Gruplama

SQL patikasında öğrendiğin her şey burada da geçerli:

```python
print(duckdb.sql("""
    SELECT city, count(*) AS orders,
           round(sum(quantity * unit_price) / 1e6, 2) AS revenue_m
    FROM 'orders.parquet'
    GROUP BY city
    ORDER BY revenue_m DESC
    LIMIT 3
"""))
```

```text
┌──────────┬────────┬───────────┐
│   city   │ orders │ revenue_m │
│ varchar  │ int64  │  double   │
├──────────┼────────┼───────────┤
│ Istanbul │ 340437 │     557.0 │
│ Ankara   │ 159984 │    260.83 │
│ Izmir    │ 129921 │     212.5 │
└──────────┴────────┴───────────┘
```

Bölüm 3'te bu sonucu parça parça okuyup `groupby` ile birleştirerek
bulmuştuk (İstanbul 557,00 milyon). DuckDB aynı işi tek bir sorguyla
yapıyor; parçalamayı kendisi düşünüyor.

`LIMIT 3` SQL Server'daki `TOP 3`'ün karşılığı.

## Sonucu pandas'a almak

Sorgunun sonucu küçükse ve pandas'la devam etmek istiyorsan `.df()`:

```python
t = duckdb.sql("""
    SELECT city, count(*) AS orders
    FROM 'orders.parquet'
    GROUP BY city
    ORDER BY orders DESC
""").df()
print(type(t).__name__)
print(t.head(3))
```

```text
DataFrame
       city  orders
0  Istanbul  340437
1    Ankara  159984
2     Izmir  129921
```

Bu, büyük veride çok kullanışlı bir iş bölümü: **büyük kısmı DuckDB
süzüp özetlesin, küçük sonucu pandas'a ver.** Bir milyon satır sekiz
satıra indi; pandas'ın işi artık kolay.

## Tabloyu tanımak: `DESCRIBE`

Bir dosyanın sütunlarını ve türlerini görmek için:

```python
print(duckdb.sql("""
    SELECT column_name, column_type
    FROM (DESCRIBE SELECT * FROM 'orders.csv')
"""))
```

```text
┌─────────────┬─────────────┐
│ column_name │ column_type │
│   varchar   │   varchar   │
├─────────────┼─────────────┤
│ order_id    │ BIGINT      │
│ order_time  │ TIMESTAMP   │
│ customer_id │ BIGINT      │
│ city        │ VARCHAR     │
│ category    │ VARCHAR     │
│ quantity    │ BIGINT      │
│ unit_price  │ DOUBLE      │
│ payment     │ VARCHAR     │
└─────────────┴─────────────┘
```

Dikkat: bu bir **CSV** dosyası ve DuckDB `order_time` sütununun tarih-saat
olduğunu kendisi anladı (`TIMESTAMP`). pandas aynı CSV'yi `str` olarak
okuyordu; DuckDB ilk satırlara bakıp türleri tahmin ediyor.

## Hızlı özet: `SUMMARIZE`

`SUMMARIZE` her sütun için en küçük, en büyük, ortalama, farklı değer sayısı
gibi bilgileri tek seferde çıkarıyor. Sonuç çok geniş olduğu için birkaç
sütununu seçiyoruz:

```python
print(duckdb.sql("""
    SELECT column_name, min, max, approx_unique, round(avg::DOUBLE, 2) AS avg
    FROM (SUMMARIZE SELECT quantity, unit_price, city FROM 'orders.csv')
"""))
```

```text
┌─────────────┬─────────┬──────────┬───────────────┬────────┐
│ column_name │   min   │   max    │ approx_unique │  avg   │
│   varchar   │ varchar │ varchar  │     int64     │ double │
├─────────────┼─────────┼──────────┼───────────────┼────────┤
│ quantity    │ 1       │ 5        │             5 │   2.22 │
│ unit_price  │ 33.69   │ 16646.99 │        216700 │ 736.87 │
│ city        │ Adana   │ Trabzon  │             7 │   NULL │
└─────────────┴─────────┴──────────┴───────────────┴────────┘
```

Bir şeye dikkat et: `approx_unique` şehir için **7** diyor, oysa 8 şehir var.
Adındaki "approx" yaklaşık demek: DuckDB farklı değerleri tek tek saymak
yerine çok az bellekle **tahmin ediyor**. Büyük veride bu tür yaklaşık
hesaplar bilerek kullanılıyor; nasıl çalıştıklarını Bölüm 9'da göreceğiz.
Kesin sayı gerekiyorsa `count(DISTINCT city)`.

`avg::DOUBLE`: `::` bir değeri başka bir türe çeviriyor. `SUMMARIZE`
ortalamayı metin olarak veriyor; yuvarlayabilmek için önce sayıya
çeviriyoruz.

## Klasörler ve joker karakter

Bölümlenmiş veride bütün dosyaları tek tek gezmek gerekmiyor. Dosya adında
`*` (joker) kullanınca DuckDB uyan bütün dosyaları tek bir tablo gibi
okuyor:

```python
print(duckdb.sql("SELECT count(*) FROM 'orders/*/*.parquet'").fetchone())
```

```text
(1000000,)
```

`hive_partitioning = true` ise klasör adlarındaki `month=...` bilgisini bir
sütun olarak geri getiriyor ve bölüm budamayı kendisi yapıyor:

```python
print(duckdb.sql("""
    SELECT month, count(*) AS orders
    FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)
    WHERE month >= '2024-11'
    GROUP BY month
    ORDER BY month
"""))
```

```text
┌─────────┬────────┐
│  month  │ orders │
│ varchar │ int64  │
├─────────┼────────┤
│ 2024-11 │  82115 │
│ 2024-12 │  85002 │
└─────────┴────────┘
```

Geçen bölümde elle yaptığımız işi (`glob`, klasör adından ay, süzme) tek bir
sorgu yaptı; Kasım ve Aralık dışındaki on klasör okunmadı.

## Neden bu kadar hızlı?

Şehir başına ciroyu dört yolla hesapladım (bu bilgisayarda, üç denemenin
en hızlısı):

| Yol | Süre |
|---|---|
| pandas, CSV | 1,78 sn |
| pandas, Parquet (3 sütun) | 0,059 sn |
| DuckDB, CSV | 0,208 sn |
| DuckDB, Parquet | 0,011 sn |

Aynı CSV'yi DuckDB pandas'tan sekiz kat hızlı işledi. Sebepleri:

1. **Yalnızca gereken sütunlar.** Sorgu `city`, `quantity` ve `unit_price`
   istiyor; DuckDB öbür beş sütunu hiç çözmüyor. Parquet'de bunlara hiç
   dokunmuyor bile.
2. **Bütün çekirdekler.** pandas bir hesabı genellikle tek çekirdekte
   yapıyor; DuckDB işi çekirdeklere bölüyor.
3. **Akarak işleme.** DuckDB dosyayı küçük yığınlar hâlinde okuyup
   işliyor; bütün tabloyu belleğe alması gerekmiyor. Gruplamada bellekte
   yalnızca grupların ara sonuçları duruyor.

Üçüncü madde büyük veri için en önemlisi: DuckDB bu yüzden belleğinden
büyük dosyaları da sorgulayabiliyor. Ara sonuçlar belleğe sığmazsa
(büyük bir sıralama ya da birleştirme gibi) onları geçici dosyalara
yazarak devam ediyor.

## Kalıcı bir veritabanı

`duckdb.sql(...)` her seferinde bellekte geçici bir veritabanı kullanıyor.
Tabloları saklamak istersen bir dosyaya bağlan:

```python
con = duckdb.connect("shop.duckdb")
con.sql("CREATE TABLE orders AS SELECT * FROM 'orders.parquet'")
print(con.sql("SELECT count(*) FROM orders").fetchone())
con.close()
```

- `duckdb.connect("shop.duckdb")`: dosya yoksa açıyor, varsa bağlanıyor.
- `CREATE TABLE ... AS SELECT ...`: sorgunun sonucunu yeni bir tablo olarak
  saklıyor.
- `con.close()`: bağlantıyı kapatıyor. Programı yeniden açıp aynı dosyaya
  bağlanınca `orders` tablosu orada duruyor.

`shop.duckdb` dosyası bir milyon siparişle 10,8 MB tuttu; DuckDB de verisini
sütun sütun ve sıkıştırarak saklıyor.

## Sonucu dosyaya yazmak: `COPY`

`COPY (sorgu) TO 'dosya'` bir sorgunun sonucunu doğrudan diske yazıyor:

```python
duckdb.sql("""
    COPY (SELECT city, count(*) AS orders FROM 'orders.parquet'
          GROUP BY city ORDER BY city)
    TO 'city_counts.csv' (HEADER)
""")
```

Aynı yolla bir CSV'yi tek komutla Parquet'ye çevirebilirsin:

```python
duckdb.sql("""
    COPY (SELECT * FROM 'orders.csv')
    TO 'from_csv.parquet' (FORMAT parquet, COMPRESSION zstd)
""")
```

Ortaya çıkan dosya 11,9 MB ve tarih sütunu `TIMESTAMP` olarak saklandı:
türleri DuckDB tahmin etti, sen hiç vermedin.

## Hata mesajları

Olmayan bir sütun yazarsan DuckDB sorguyu çalıştırmadan önce söylüyor:

```text
BinderException: Binder Error: Referenced column "nosuch" not found in FROM clause!
```

"Binder" sorgudaki adları tablolara bağlayan aşama; bu hata neredeyse her
zaman bir yazım hatası ya da yanlış dosya demek.

## SQL Server'dan farkları

SQL patikasındaki T-SQL ile DuckDB'nin SQL'i büyük ölçüde aynı. Sık
karşılaşacağın farklar:

| SQL Server (T-SQL) | DuckDB |
|---|---|
| `SELECT TOP 3 ...` | `... LIMIT 3` |
| `FORMAT(tarih, 'yyyy-MM')` | `strftime(tarih, '%Y-%m')` |
| Tablo bir veritabanında | `FROM 'dosya.parquet'` da olur |
| `[sütun adı]` | `"sütun adı"` |

## Özet

- DuckDB Python'un içinde çalışan, sunucusuz bir analiz veritabanı.
- `duckdb.sql("... FROM 'orders.parquet'")`: dosya adı tablo yerine geçiyor;
  CSV de olur.
- `.fetchall()` Python listesi, `.df()` pandas tablosu veriyor. Büyük işi
  DuckDB'ye, küçük sonucu pandas'a ver.
- `DESCRIBE` sütunları ve türleri, `SUMMARIZE` hızlı istatistikleri
  gösteriyor; DuckDB CSV'deki türleri de tahmin ediyor.
- `'klasör/*/*.parquet'` birçok dosyayı tek tablo gibi okuyor;
  `hive_partitioning = true` bölüm sütununu geri getirip budamayı yapıyor.
- Yalnızca gereken sütunları, bütün çekirdeklerle ve akarak işlediği için
  hızlı: bu ölçümde CSV'de pandas'tan sekiz kat.
- `duckdb.connect("dosya.duckdb")` kalıcı veritabanı, `COPY ... TO` sonucu
  dosyaya yazıyor.
