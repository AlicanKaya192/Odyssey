# Bitirme Projesi

Bu bölümde patikadaki araçları tek bir işte bir araya getiriyoruz. Yeni bir
kavram yok; amaç, büyük bir veriyle karşılaşınca **hangi sırayla, neye
bakarak** karar verildiğini baştan sona bir kez yaşamak.

## Senaryo

Bir mağaza her gece bütün yılın siparişlerini bir CSV dosyası olarak
veriyor: bir milyon satır. Yönetici şunları soruyor:

1. Her ayın şehir şehir cirosu ne?
2. Bu sorulara her gün, beklemeden cevap verebilir miyiz?
3. Sonuçlara güvenebilir miyiz?

Elimizde tek bir dizüstü bilgisayar var. Kurduğumuz şeyin adı **veri hattı**
(*data pipeline*): ham veriyi alıp sorulara hazır hâle getiren adımlar dizisi.

<figure class="fig">
  <div class="flow">
    <span class="node">Ölç</span><span class="arrow">→</span>
    <span class="node">Parquet</span><span class="arrow">→</span>
    <span class="node">Bölümle</span><span class="arrow">→</span>
    <span class="node">Sorgula</span><span class="arrow">→</span>
    <span class="node acc">Doğrula</span>
  </div>
  <figcaption>Her adım bir öncekinin çıktısını kullanıyor; her adımın arkasında patikadan bir bölüm var.</figcaption>
</figure>

## 1. Önce ölç

Bölüm 1'in kuralı: tahmin etme, ölç. Dosyanın tamamını açmadan önce boyutuna
ve küçük bir örneğin belleğine bakıyoruz:

```python
import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
print(round(os.path.getsize("orders.csv") / 1024**2, 1), "MB on disk")

sample = pd.read_csv("orders.csv", nrows=10_000)
per_row = sample.memory_usage(deep=True).sum() / len(sample)
print(round(per_row * 1_000_000 / 1024**2, 1), "MB in memory (estimate)")
```

```text
61.1 MB on disk
95.9 MB in memory (estimate)
```

On bin satırın satır başına belleği, bir milyonla çarpılınca tamamının
tahmini çıkıyor. Diskteki dosyadan büyük: metin sütunları bellekte yer
kaplıyor (Bölüm 1).

Bölüm 2'deki türlerle aynı tahmin:

```python
DTYPES = {"order_id": "int32", "customer_id": "int32", "quantity": "int8",
          "city": "category", "category": "category", "payment": "category"}
typed = pd.read_csv("orders.csv", nrows=10_000, dtype=DTYPES)
per_row = typed.memory_usage(deep=True).sum() / len(typed)
print(round(per_row * 1_000_000 / 1024**2, 1), "MB with types (estimate)")
```

```text
44.9 MB with types (estimate)
```

Bellek yarıdan azına iniyor. Tahmin de güvenilir: dosyanın tamamı bu türlerle
okununca 44,8 MB çıkıyor. **Karar:** bu boyut belleğe sığıyor, ama
her gün aynı CSV'yi baştan okumak boşa iş. Veriyi bir kez, sorulara uygun bir
biçime çevireceğiz.

## 2. Parquet'e çevir, parça parça

CSV'yi tek seferde açmak yerine 250 000 satırlık parçalarla okuyup (Bölüm 3)
tek bir Parquet dosyasına yazıyoruz (Bölüm 5). Her parça dosyada bir satır
grubu oluyor. Ay sütununu da bu sırada ekliyoruz; sonraki adım ona göre
bölecek.

```python
import pyarrow as pa
import pyarrow.parquet as pq

NUMERIC = {"order_id": "int32", "customer_id": "int32", "quantity": "int8"}
writer = None
for chunk in pd.read_csv("orders.csv", chunksize=250_000, dtype=NUMERIC):
    chunk["month"] = chunk["order_time"].str[:7]
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema, compression="zstd")
    writer.write_table(table)
writer.close()

pf = pq.ParquetFile("orders.parquet")
print(pf.metadata.num_rows, "rows,", pf.num_row_groups, "row groups")
print(round(os.path.getsize("orders.parquet") / 1024**2, 1), "MB")
```

```text
1000000 rows, 4 row groups
16.4 MB
```

Bellekte aynı anda yalnızca bir parça var; dosya bir milyar satır olsaydı da
kod aynı kalırdı. Parquet dosyası CSV'nin üçte birinden de küçük. Metin
sütunlarına `category` vermedik: Parquet tekrar eden değerleri zaten
sözlükle kodluyor (Bölüm 5).

## 3. Aya göre bölümle

Soruların çoğu "şu ay" diye başlıyor. Veriyi ay klasörlerine ayırırsak
(Bölüm 6) bir ayın sorusu yalnızca o ayın dosyasını okur:

```python
orders = pd.read_parquet("orders.parquet")
for month, part in orders.groupby("month"):
    folder = f"lake/month={month}"
    os.makedirs(folder, exist_ok=True)
    part.drop(columns="month").to_parquet(f"{folder}/part-0.parquet", index=False)

print(sorted(os.listdir("lake"))[:3], len(os.listdir("lake")))
```

```text
['month=2024-01', 'month=2024-02', 'month=2024-03'] 12
```

`month=2024-01` biçimindeki klasör adı Hive bölümlemesi: ay sütunu dosyanın
içinde değil, klasörün adında duruyor. Böyle bir klasör düzenine
**veri gölü** (*data lake*) de deniyor.

## 4. DuckDB ile sorgula

Gölü DuckDB ile, tek bir tablo gibi sorguluyoruz (Bölüm 7):

```python
import duckdb

lake = "read_parquet('lake/*/*.parquet', hive_partitioning = true)"
print(duckdb.sql(f"""
    SELECT city, round(sum(quantity * unit_price), 2) AS revenue
    FROM {lake}
    WHERE month = '2024-03'
    GROUP BY city
    ORDER BY revenue DESC
    LIMIT 3
""").fetchall())
```

```text
[('Istanbul', 47440696.91), ('Ankara', 22131451.91), ('Izmir', 17415485.42)]
```

DuckDB'nin gerçekten tek klasörü okuduğunu planından görebiliriz.
`EXPLAIN ANALYZE` sorguyu çalıştırıp her adımın ayrıntısını uzun bir metin
olarak veriyor. O metinden yalnızca taranan dosya bilgisini `re.search` ile
alıyoruz: `re.search` metinde bir kalıp arıyor, kalıptaki `\d+` "bir ya da
daha çok rakam" demek.

```python
import re

plan = duckdb.sql(f"""
    EXPLAIN ANALYZE SELECT count(*) FROM {lake} WHERE month = '2024-03'
""").fetchall()[0][1]
print(re.search(r"Scanning Files: \d+/\d+", plan).group())
```

```text
Scanning Files: 1/12
```

On iki dosyadan biri. Yıl büyüdükçe, örneğin on yıllık veride, bir ayın
sorusu yine tek dosya okur.

## 5. Doğrula

Bir sayıyı yöneticiye vermeden önce onu **başka bir yoldan** da
hesaplıyoruz. İkinci yol olarak Parquet dosyasının satır gruplarını tek tek
okuyup şehir başına kısmi toplamlar çıkarıyor ve birleştiriyoruz: Bölüm 12'deki
birleştiricinin aynısı. Sonra DuckDB'nin sonucuyla karşılaştırıyoruz:

```python
totals = {}
for i in range(pf.num_row_groups):
    part = pf.read_row_group(i, columns=["city", "quantity", "unit_price"]).to_pandas()
    part["revenue"] = part["quantity"] * part["unit_price"]
    for city, value in part.groupby("city")["revenue"].sum().items():
        totals[city] = totals.get(city, 0.0) + value

exact = dict(duckdb.sql("""
    SELECT city, sum(quantity * unit_price) FROM 'orders.parquet' GROUP BY city
""").fetchall())
print(all(abs(totals[c] - exact[c]) < 0.01 for c in exact))
print(len(totals), "cities")
```

```text
True
8 cities
```

İki yol aynı sonucu veriyor. `==` yerine "farkı 0,01'den küçük" diye
karşılaştırdık: ondalık sayıları farklı sırayla toplamak son basamaklarda
çok küçük farklar bırakabiliyor.

Doğrulamanın ikinci yüzü **hızlı tahmin**. Yönetici bazen kesin sayıyı değil,
hızlı bir fikri istiyor. Bölüm 9'daki örneklem, verinin yüzde biriyle
kategori başına ortalama sipariş tutarını tahmin ediyor:

```python
orders["revenue"] = orders["quantity"] * orders["unit_price"]
sample = orders.sample(frac=0.01, random_state=1)
estimate = sample.groupby("category")["revenue"].mean()
true = orders.groupby("category")["revenue"].mean()
print(((estimate - true).abs() / true * 100).round(1))
```

```text
category
books          0.1
clothing       2.9
electronics    1.5
home           2.1
sports         0.1
toys           2.5
Name: revenue, dtype: float64
```

Bu örneklemde hatalar yüzde birkaç. Hızlı bir fikir için yeterli;
yayımlanacak rapor için kesin sorgu çalıştırılıyor.

## Hangi adım, hangi bölüm?

| Adım | Ne yaptık | Bölüm |
|---|---|---|
| Ölç | Örnekten bellek tahmini | 1 |
| Türler | `int32`, `int8`, `category` | 2 |
| Parça parça | `chunksize` ile okuma | 3 |
| Parquet | Satır grupları, `zstd` | 4, 5 |
| Bölümle | Ay klasörleri | 6 |
| Sorgula | DuckDB, dosyadan SQL | 7, 8 |
| Tahmin | %1 örneklem | 9 |
| Doğrula | Kısmi toplam + birleştirme | 12 |

## Projeyi büyütmek

Bu hat tek bilgisayarda çalıştı. Koşullar değişince adımlar aynı kalıyor,
yalnızca araç değişiyor:

- **Veri yüz kat büyürse:** çevirme ve bölümleme adımlarını dask (Bölüm 11)
  ya da bir Spark kümesi (Bölüm 13) yapıyor; Parquet ve bölümleme aynı.
- **Siparişler canlı gelirse:** gece CSV'si yerine bir Kafka konusu; anlık
  sorular pencerelerle (Bölüm 14), gün sonunda olaylar yine Parquet gölüne
  yazılıyor.
- **Veri bulutta durursa:** göl bir bulut deposunda (Amazon S3 gibi) duruyor;
  DuckDB ve Spark oradaki Parquet dosyalarını aynı yazımla okuyabiliyor.

Bu hattın en önemli kararı ilk adımdaydı: **ölçmek**. Bir milyon satır bu
bilgisayarın belleğine sığdı; yine de bölümleme ve Parquet her günkü soruyu
ucuzlattı. Büyük veri bir boyut değil, bir alışkanlık: önce ölç, sonra
yalnızca gerekeni oku.

## Özet

- Veri hattı: ölç → çevir → bölümle → sorgula → doğrula.
- Ölçerken küçük bir örnekten tahmin et; türlerle bellek yarıdan aza indi.
- CSV'yi parça parça Parquet'e çevirmek belleği sabit tutuyor ve dosyayı
  küçültüyor.
- Ay klasörleriyle bir ayın sorusu 12 dosyadan yalnızca birini okuyor.
- Her sonucu ikinci bir yoldan doğrula; ondalıkları toleransla karşılaştır.
- Hızlı tahmin için örneklem, rapor için kesin sorgu.
