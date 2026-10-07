# DuckDB ve pandas Birlikte

DuckDB ile pandas rakip değil, ortak. DuckDB bir pandas tablosunu **değişken
adıyla** doğrudan sorgulayabiliyor; sonucu da tek satırla pandas'a geri
veriyor. Böylece bir analizin her adımında o adıma en uygun aracı
seçebiliyorsun: büyük dosyayı süzmek ve birleştirmek için SQL, son
biçimlendirme ve grafik için pandas.

Bu bölümde iki dünya arasında gidip gelmeyi, SQL'in pandas'ta zahmetli
olan işlerini (birleştirme, pencere fonksiyonları) ve hangi durumda hangi
aracın gerçekten daha hızlı olduğunu ölçerek göreceğiz.

Örneklerde bir milyon sipariş hem bellekte (`orders`) hem diskte
(`orders.parquet`) duruyor:

```python
import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(1_000_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)
```

## Tabloyu adıyla sorgulamak

`FROM` sonrasına bir pandas değişkeninin adını yazmak yetiyor:

```python
print(duckdb.sql("""
    SELECT city, count(*) AS n
    FROM orders
    WHERE quantity >= 4
    GROUP BY city
    ORDER BY n DESC
    LIMIT 3
"""))
```

```text
┌──────────┬───────┐
│   city   │   n   │
│ varchar  │ int64 │
├──────────┼───────┤
│ Istanbul │ 75382 │
│ Ankara   │ 35488 │
│ Izmir    │ 28806 │
└──────────┴───────┘
```

DuckDB `orders` adında bir tablo bulamayınca Python'da bu adla bir değişken
arıyor; bulduğu `DataFrame`'i tablo gibi okuyor. Böyle bir değişken de yoksa
hata veriyor:

```text
CatalogException: Catalog Error: Table with name no_such_frame does not exist!
```

## Dosya ile tabloyu birleştirmek

Müşteri bilgisi küçük bir pandas tablosunda, siparişler büyük bir Parquet
dosyasında olsun. Her müşterinin bir segmenti var (`new`, `regular`, `vip`):

```python
ids = pd.RangeIndex(1, 250_000)
customers = pd.DataFrame({
    "customer_id": ids,
    "segment": pd.Series(["new", "regular", "vip"]).iloc[ids % 3].values,
})
```

İkisini tek bir SQL sorgusunda birleştirelim:

```python
print(duckdb.sql("""
    SELECT c.segment, count(*) AS orders, round(avg(o.unit_price), 2) AS avg_price
    FROM 'orders.parquet' AS o
    JOIN customers AS c USING (customer_id)
    GROUP BY c.segment
    ORDER BY c.segment
"""))
```

```text
┌─────────┬────────┬───────────┐
│ segment │ orders │ avg_price │
│ varchar │ int64  │  double   │
├─────────┼────────┼───────────┤
│ new     │ 333337 │    737.81 │
│ regular │ 333859 │    735.27 │
│ vip     │ 332804 │    737.53 │
└─────────┴────────┴───────────┘
```

- `AS o`, `AS c`: tablolara kısa takma ad.
- `JOIN ... USING (customer_id)`: iki tablodaki aynı adlı sütuna göre
  birleştir. SQL patikasındaki `ON o.customer_id = c.customer_id`'nin kısa
  yazımı.
- Bir taraf diskteki dosya, öbür taraf bellekteki tablo; DuckDB için fark
  yok.

## Pencere fonksiyonları ve `QUALIFY`

"Her müşterinin **ilk** siparişi" pandas'ta sıralama, gruplama ve süzme
gerektiren bir iş. SQL'de pencere fonksiyonuyla tek bir koşul:

```python
print(duckdb.sql("""
    SELECT customer_id, order_id, order_time
    FROM 'orders.parquet'
    QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1
    ORDER BY customer_id
    LIMIT 3
"""))
```

```text
┌─────────────┬──────────┬─────────────────────┐
│ customer_id │ order_id │     order_time      │
│    int64    │  int64   │      timestamp      │
├─────────────┼──────────┼─────────────────────┤
│           1 │    47287 │ 2024-01-18 06:16:44 │
│           2 │   177677 │ 2024-03-06 01:03:09 │
│           3 │   180262 │ 2024-03-06 23:25:00 │
└─────────────┴──────────┴─────────────────────┘
```

- `row_number() OVER (PARTITION BY customer_id ORDER BY order_time)`: her
  müşterinin siparişlerini zamana göre sıralayıp 1, 2, 3 … diye numaralıyor
  (SQL patikasındaki pencere fonksiyonları).
- `QUALIFY`: pencere fonksiyonunun sonucuna göre süzüyor. `WHERE` pencere
  fonksiyonunu göremiyor; SQL Server'da bunun için alt sorgu yazıyordun,
  DuckDB'de `QUALIFY` yetiyor.

Toplam 245 461 müşteri var ve sorgu her biri için tam bir satır veriyor.

Pencere, gruplamanın sonucunun üstünde de çalışıyor. Aylık ciro ve o ana
kadarki birikimli toplam:

```python
print(duckdb.sql("""
    SELECT strftime(order_time, '%Y-%m') AS month,
           round(sum(quantity * unit_price) / 1e6, 1) AS revenue_m,
           round(sum(sum(quantity * unit_price))
                 OVER (ORDER BY strftime(order_time, '%Y-%m')) / 1e6, 1) AS running_m
    FROM 'orders.parquet'
    GROUP BY month
    ORDER BY month
    LIMIT 4
"""))
```

```text
┌─────────┬───────────┬───────────┐
│  month  │ revenue_m │ running_m │
│ varchar │  double   │  double   │
├─────────┼───────────┼───────────┤
│ 2024-01 │     137.9 │     137.9 │
│ 2024-02 │     129.9 │     267.8 │
│ 2024-03 │     138.5 │     406.3 │
│ 2024-04 │     134.0 │     540.4 │
└─────────┴───────────┴───────────┘
```

`sum(sum(...)) OVER (...)`: içteki `sum` ayın cirosu, dıştaki `sum ... OVER`
o aya kadarki ayların toplamı.

## Parametreli sorgu

Sorguya dışarıdan bir değer koymak gerekiyorsa metni birleştirerek değil,
**soru işaretiyle** ver:

```python
def city_orders(city):
    return duckdb.execute(
        "SELECT count(*) FROM 'orders.parquet' WHERE city = ?", [city]
    ).fetchone()[0]

print(city_orders("Izmir"), city_orders("Konya"))
print(city_orders("Izmir' OR '1'='1"))
```

```text
129921 69896
0
```

- `duckdb.execute(sorgu, [değerler])`: her `?` yerine listedeki sıradaki
  değer konuyor.
- Değer sorgunun bir parçası olarak değil, **veri olarak** gidiyor. Son
  satırdaki kötü niyetli metin sorguyu bozamadı; böyle bir şehir olmadığı
  için 0 döndü. f-string ile birleştirseydin `OR '1'='1'` sorgunun parçası
  olur ve bütün siparişleri sayardı (bu makinede denendi: 1 000 000). Bu,
  Python ve API patikalarında
  gördüğün **SQL enjeksiyonu** saldırısının aynısı.

## Bir sonucu başka bir sorguda kullanmak

`duckdb.sql(...)` sonucunu bir değişkene koyarsan, o değişkeni de bir sonraki
sorguda tablo gibi kullanabilirsin:

```python
cash = duckdb.sql("SELECT * FROM 'orders.parquet' WHERE payment = 'cash'")
print(duckdb.sql("SELECT count(*), round(avg(unit_price), 2) FROM cash").fetchall())
```

```text
[(80480, 740.75)]
```

`cash` henüz bir tablo değil, bir **tarif**: sorgu ancak kullanıldığında
çalışıyor. Uzun bir analizi okunur adımlara bölmenin rahat bir yolu.

## DuckDB özetlesin, pandas biçimlendirsin

Büyük işi DuckDB yapsın, küçük sonucu pandas'ın rahat araçlarıyla
(`pivot`, oran, grafik) işle:

```python
monthly = duckdb.sql("""
    SELECT strftime(order_time, '%Y-%m') AS month, category,
           sum(quantity * unit_price) AS revenue
    FROM 'orders.parquet'
    GROUP BY month, category
""").df()
table = monthly.pivot(index="month", columns="category", values="revenue")
share = (table.div(table.sum(axis=1), axis=0) * 100).round(1)
print(share.head(3))
```

```text
category  books  clothing  electronics  home  sports  toys
month                                                     
2024-01     5.8      16.8         48.0  12.9    11.0   5.6
2024-02     5.7      16.6         48.7  12.7    10.8   5.5
2024-03     5.7      16.7         48.1  13.0    10.8   5.6
```

DuckDB bir milyon satırı 72 satıra (12 ay × 6 kategori) indirdi; pandas da
onları ay × kategori tablosuna çevirip her ayın içindeki payları hesapladı.
Elektronik cironun neredeyse yarısı.

## Hangisi ne zaman? Ölçerek bakalım

"DuckDB her zaman daha hızlı" sanmak kolay. Aynı işleri bu bilgisayarda
ölçtüm (üç denemenin en hızlısı, bir milyon sipariş):

| İş | pandas | DuckDB |
|---|---|---|
| Bellekteki tablo, şehir `str`: şehir başına ciro | 0,044 sn | 0,132 sn |
| Bellekteki tablo, şehir `category`: aynı iş | 0,019 sn | 0,003 sn |
| Her müşterinin ilk siparişi | 0,283 sn | 0,514 sn |
| CSV dosyasından şehir başına ciro (Bölüm 7) | 1,78 sn | 0,208 sn |

Buradan çıkanlar:

1. **Veri dosyadaysa DuckDB.** Okumayı ve hesabı birlikte, yalnızca gereken
   sütunlarla ve bütün çekirdeklerle yapıyor.
2. **Veri zaten bellekte, doğru türlerdeyse ikisi de hızlı.** pandas'ın
   bellekteki bir tabloda yaptığı işi DuckDB'ye taşımak her zaman kazanç
   değil.
3. **DuckDB'ye pandas tablosu verirken metni `category` yap.** pandas'ın
   `str` sütununu okumak DuckDB için pahalı; `category` ile aynı iş 0,132
   sn'den 0,003 sn'ye indi. Bölüm 2'deki tür seçimi burada da karşılığını
   veriyor.
4. **Sonucu pandas'a çevirmenin bir bedeli var.** İlk sipariş sorgusu
   245 461 satırlık bir sonucu `DataFrame`'e çevirdiği için yavaş kaldı. Sonuç
   büyükse onu pandas'a almadan DuckDB'de işlemeye devam et ya da doğrudan
   dosyaya yaz (`COPY`).

Seçim hız kadar **okunurlukla** da ilgili: birleştirme ve pencere işleri
SQL'de genellikle daha kısa ve anlaşılır; adım adım veri temizliği ve grafik
pandas'ta daha rahat.

## Özet

- DuckDB bir pandas tablosunu değişken adıyla sorguluyor: `FROM orders`.
- Bir sorguda dosya ile bellekteki tablo birleştirilebiliyor
  (`JOIN ... USING (...)`).
- `QUALIFY` pencere fonksiyonunun sonucuna göre süzüyor: "her müşterinin ilk
  siparişi" tek koşul.
- Dışarıdan gelen değer `?` ile verilir (`duckdb.execute(sorgu, [değer])`);
  metin birleştirmek SQL enjeksiyonuna kapı açar.
- Bir sonucu değişkene koyup sonraki sorguda tablo gibi kullanabilirsin.
- Dosyadan okurken DuckDB çok hızlı; bellekteki tabloda pandas da hızlı.
  DuckDB'ye tablo verirken metni `category` yap; büyük sonucu pandas'a
  çevirmekten kaçın.
