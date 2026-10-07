# Parquet

Geçen bölümde Parquet'nin küçük ve hızlı olduğunu gördük. Bu bölümde
**neden** öyle olduğuna bakıyoruz. Parquet dosyasının içi, okuyan programın
gereksiz kısımları **hiç açmadan atlayabileceği** şekilde düzenlenmiş. Bu
düzeni bilirsen dosyayı ona göre yazabilir, okurken de yalnızca gerekene
dokunabilirsin.

Örnekler bir milyon siparişle çalışıyor:

```python
import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(1_000_000)
df["order_time"] = pd.to_datetime(df["order_time"])
```

## Dosyanın katmanları

Bir Parquet dosyası iç içe dört katmandan oluşuyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Dosya</span><span>Satır gruplarının art arda dizilişi</span></div>
    <div class="anat-row"><span>Satır grubu</span><span>Örneğin 100 000 sipariş; her grup kendi başına okunabilir</span></div>
    <div class="anat-row"><span>Sütun parçası</span><span>Bir gruptaki tek bir sütun: o 100 000 siparişin <code>city</code> değerleri</span></div>
    <div class="anat-row"><span>Sayfa</span><span>Sütun parçasının küçük bir bölümü; sıkıştırma birimi</span></div>
    <div class="anat-row"><span>Altbilgi</span><span>Dosyanın sonunda: şema, grupların yeri, her sütun parçasının en küçük ve en büyük değeri</span></div>
  </div>
  <figcaption>Okuyan program önce küçük altbilgiyi okuyor, sonra yalnızca gereken gruplara ve sütunlara gidiyor.</figcaption>
</figure>

1. **Dosya** satır gruplarına bölünmüş.
2. **Satır grubu** (*row group*) belli sayıda satırı tutuyor: örneğin
   100 000 sipariş.
3. Satır grubunun içinde her sütun ayrı bir **sütun parçası** (*column
   chunk*): o 100 000 siparişin yalnızca `city` değerleri gibi.
4. Sütun parçası da küçük **sayfalara** (*page*) bölünüyor; okuma ve
   sıkıştırma birimi bunlar.

Dosyanın en sonunda bir **altbilgi** (*footer*) var: hangi satır grubunun
dosyanın neresinde başladığı, her sütunun türü ve her sütun parçası için
**özet istatistikler**. Okuyan program önce bu küçük altbilgiyi okuyor,
sonra yalnızca gereken parçalara gidiyor.

## Satır grupları

pandas'ın `to_parquet`'i bir milyon satırı varsayılan olarak tek satır
grubuna koyuyor. `row_group_size=` ile daha küçük gruplar isteyebilirsin:

```python
df.to_parquet("default.parquet")
df.to_parquet("orders.parquet", row_group_size=100_000)
for name in ["default.parquet", "orders.parquet"]:
    f = pq.ParquetFile(name)
    print(name, f.metadata.num_row_groups, f.metadata.row_group(0).num_rows)
```

```text
default.parquet 1 1000000
orders.parquet 10 100000
```

`pq.ParquetFile(...)` dosyayı açıyor ama verisini okumuyor; `metadata`
altbilgideki özet. Bu çağrı dosyanın boyutundan bağımsız olarak hızlı.

## Her grubun istatistikleri

Altbilgi her satır grubunun her sütunu için en küçük ve en büyük değeri
saklıyor. Sipariş zamanı, fiyat ve şehir için bakalım:

```python
f = pq.ParquetFile("orders.parquet")
names = f.schema_arrow.names
t = names.index("order_time")
c = names.index("city")
for i in range(f.metadata.num_row_groups):
    rg = f.metadata.row_group(i)
    times = rg.column(t).statistics
    cities = rg.column(c).statistics
    print(i, times.min.date(), times.max.date(), cities.min, cities.max)
```

```text
0 2024-01-01 2024-02-06 Adana Trabzon
1 2024-02-06 2024-03-14 Adana Trabzon
2 2024-03-14 2024-04-19 Adana Trabzon
3 2024-04-19 2024-05-26 Adana Trabzon
4 2024-05-26 2024-07-02 Adana Trabzon
5 2024-07-02 2024-08-07 Adana Trabzon
6 2024-08-07 2024-09-13 Adana Trabzon
7 2024-09-13 2024-10-19 Adana Trabzon
8 2024-10-19 2024-11-25 Adana Trabzon
9 2024-11-25 2024-12-31 Adana Trabzon
```

- Siparişler zaman sırasıyla üretildiği için her grup yılın ayrı bir
  dilimini tutuyor: 0. grup Ocak başı, 9. grup Aralık.
- Şehirler ise her grupta karışık: her grubun en küçüğü `Adana`, en
  büyüğü `Trabzon`.

## Okumadan atlamak

Yalnızca Aralık siparişlerini istediğini düşün. İstatistiklere bakınca
cevap belli: en büyük zamanı 1 Aralık'tan küçük olan grupta Aralık
siparişi **olamaz**. O grupları açmaya gerek yok.

```python
start = pd.Timestamp("2024-12-01")
keep = [i for i in range(f.metadata.num_row_groups)
        if f.metadata.row_group(i).column(t).statistics.max >= start]
print(keep)
parts = [f.read_row_group(i).to_pandas() for i in keep]
december = pd.concat(parts)
december = december[december["order_time"] >= start]
print(len(december))
```

```text
[9]
85002
```

On gruptan yalnızca biri okundu. Seçilen grubun içinde Kasım sonundan
kalma satırlar da olduğu için en sonda yine süzdük.

Bu işe **istatistikle atlama** (*predicate pushdown*, "koşulu veriye doğru
itmek") deniyor. `read_parquet` bunu `filters=` ile kendisi yapıyor:

```python
december = pd.read_parquet(
    "orders.parquet",
    filters=[("order_time", ">=", pd.Timestamp("2024-12-01"))],
)
```

Bu bilgisayarda bütün dosyayı okumak 0,036 saniye, Aralık'ı `filters=` ile
okumak 0,014 saniye sürdü. Dosya ne kadar büyükse atlanan kısım da o kadar
büyük.

## Sıra her şeyi değiştirir

Aynı numarayı şehir için deneyelim: "yalnızca İzmir". İstatistiklerde her
grup `Adana` ile `Trabzon` arasında; İzmir her grupta **olabilir**. Hiçbir
grup atlanamıyor.

Dosyayı yazmadan önce şehre göre sıralarsak durum değişiyor:

```python
by_city = df.sort_values("city")
by_city.to_parquet("by_city.parquet", row_group_size=100_000)
f2 = pq.ParquetFile("by_city.parquet")
c = f2.schema_arrow.names.index("city")
for i in range(f2.metadata.num_row_groups):
    s = f2.metadata.row_group(i).column(c).statistics
    print(i, s.min, s.max)
```

```text
0 Adana Ankara
1 Ankara Ankara
2 Ankara Antalya
3 Antalya Bursa
4 Bursa Istanbul
5 Istanbul Istanbul
6 Istanbul Istanbul
7 Istanbul Izmir
8 Izmir Konya
9 Konya Trabzon
```

Artık İzmir yalnızca 7. ve 8. gruplarda olabilir; diğer sekiz grup
atlanıyor. Ama bedava değil: zaman sırası bozulduğu için dosya 26,0 MB'tan
31,7 MB'a büyüdü (sıralı zaman ve sipariş numarası daha iyi sıkışıyordu).

Kural: dosyayı **en sık süzeceğin sütuna göre sıralı** yaz. Zaman serisi
gibi verilerde bu çoğu zaman zaten zaman.

## Sütun parçaları ve sözlük kodlaması

Bir satır grubunun içine bakıp her sütun parçasının diskte kaç bayt
tuttuğunu görelim:

```python
rg = pq.ParquetFile("orders.parquet").metadata.row_group(0)
for j in range(rg.num_columns):
    col = rg.column(j)
    print(col.path_in_schema, col.total_compressed_size)
```

```text
order_id 603354
order_time 848893
customer_id 596194
city 38081
category 38050
quantity 38141
unit_price 532649
payment 25650
```

100 000 satırda `city` 38 081 bayt, `order_time` ise 848 893 bayt: yirmi
kattan fazla. Neden? Parquet tekrar
eden değerleri **sözlük kodlamasıyla** (*dictionary encoding*) saklıyor:
farklı değerlerin listesi bir kez, satırlarda yalnızca numaraları. Geçen
bölümlerdeki `category` türünün dosyadaki karşılığı bu. Neredeyse her değeri
farklı olan `order_time`'da sözlük işe yaramıyor.

## Parça parça okumak

Parquet'de "parça" hazır: satır grupları. Bir grubu tek başına okumak:

```python
g = pq.ParquetFile("orders.parquet").read_row_group(3).to_pandas()
print(len(g), g["order_id"].iloc[0], g["order_id"].iloc[-1])
```

```text
100000 300001 400000
```

`iter_batches` ise dosyayı istediğin büyüklükte parçalar hâlinde veriyor;
`read_csv(chunksize=...)`'nin Parquet'deki karşılığı:

```python
total = 0
for batch in pq.ParquetFile("orders.parquet").iter_batches(
        batch_size=250_000, columns=["quantity", "unit_price"]):
    part = batch.to_pandas()
    total += (part["quantity"] * part["unit_price"]).sum()
print(round(total, 2))
```

```text
1635737361.77
```

`columns=` burada da çalışıyor: yalnızca iki sütun okunuyor.

## Parça parça yazmak: `ParquetWriter`

Geçen bölümde gördük: `to_parquet` dosyanın sonuna eklemiyor. Belleğe
sığmayan bir CSV'yi tek bir Parquet dosyasına çevirmek için
`pyarrow.parquet.ParquetWriter` var: dosyayı bir kez açıyorsun, her parçayı
yeni bir satır grubu olarak yazıyorsun, en sonda kapatıyorsun.

```python
import pyarrow as pa
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
writer = None
for chunk in pd.read_csv("orders.csv", chunksize=200_000, parse_dates=["order_time"]):
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema)
    writer.write_table(table)
writer.close()
```

- `pa.Table.from_pandas(...)`: pandas tablosunu `pyarrow`'un kendi tablo
  türüne çeviriyor. `preserve_index=False` indeksi dosyaya koymuyor.
- `table.schema`: sütunlar ve türleri. Yazıcı ilk parçanın şemasıyla
  açılıyor.
- Her `write_table` bir satır grubu ekliyor: bir milyon satır, beş grup.
- `writer.close()` altbilgiyi yazıyor. Kapatmadan okumaya çalışırsan
  `ArrowInvalid: ... Parquet magic bytes not found in footer` hatası
  alırsın: dosyanın sonunda altbilgi henüz yok.

Bellekte her an tek bir parça var; CSV ne kadar büyük olursa olsun.

Her parçanın şeması ilkiyle **aynı** olmalı. Bir sütun bir parçada tam sayı,
başka bir parçada ondalıklı gelirse `write_table` hata veriyor:
`ValueError: Table schema does not match schema used to create file`. Bunu
önlemek için türleri `read_csv`'ye `dtype=` ile sabit ver.

## Özet

- Parquet: dosya → satır grupları → sütun parçaları → sayfalar; en sonda
  türleri ve istatistikleri tutan altbilgi.
- `pq.ParquetFile(yol).metadata` dosyayı okumadan satır, grup ve sütun
  bilgisini veriyor.
- `row_group_size=` satır grubu büyüklüğünü seçiyor.
- Her grubun her sütunu için en küçük ve en büyük değer saklanıyor; koşula
  uymayacağı belli olan gruplar okunmadan atlanıyor (`filters=`).
- Atlama ancak veri süzülen sütuna göre **sıralıysa** işe yarıyor; sıralamak
  sıkıştırmayı değiştirebiliyor.
- Tekrar eden değerler sözlük kodlamasıyla çok küçük tutuyor.
- `read_row_group`, `iter_batches` ile parça parça okunuyor;
  `ParquetWriter` ile parça parça yazılıyor, şema her parçada aynı olmalı.
