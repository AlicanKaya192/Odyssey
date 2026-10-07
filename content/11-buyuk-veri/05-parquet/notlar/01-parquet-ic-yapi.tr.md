Parquet dosyasının içine bakmak ve onu parça parça okuyup yazmak için
gereken her şey.

## Katmanlar

| Katman | Ne tutuyor |
|---|---|
| Dosya | Satır grupları + en sonda altbilgi |
| Satır grubu | Belli sayıda satır (ör. 100 000) |
| Sütun parçası | Bir satır grubundaki tek bir sütun |
| Sayfa | Sütun parçasının küçük bir bölümü |
| Altbilgi | Şema, grupların yeri, her sütun parçasının istatistikleri |

## Dosyaya bakmak

```python
import pyarrow.parquet as pq

f = pq.ParquetFile("orders.parquet")
f.metadata.num_rows
f.metadata.num_row_groups
f.schema_arrow                       # sütunlar ve türleri
f.schema_arrow.names                 # sütun adları

rg = f.metadata.row_group(0)         # 0. satır grubu
rg.num_rows
col = rg.column(2)                   # o grubun 2. sütun parçası
col.path_in_schema                   # sütunun adı
col.statistics.min, col.statistics.max
col.statistics.null_count
col.total_compressed_size            # diskte bayt
col.compression                      # SNAPPY, ZSTD ...
```

## Okumak

```python
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
f.read_row_group(3).to_pandas()
for batch in f.iter_batches(batch_size=250_000, columns=[...]):
    part = batch.to_pandas()
```

## `filters=`

```python
pd.read_parquet("orders.parquet", filters=[("order_time", ">=", baslangic)])
```

- Her koşul bir üçlü: `(sütun, işlem, değer)`.
- İşlemler: `==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not in`.
- Bir listedeki koşullar **ve** ile bağlanıyor:
  `[("city", "==", "Izmir"), ("quantity", ">=", 3)]`.
- Listelerin listesi **veya** demek:
  `[[("city", "==", "Izmir")], [("city", "==", "Bursa")]]`.

## Yazmak

```python
df.to_parquet("orders.parquet", row_group_size=100_000, compression="zstd")
```

Parça parça:

```python
import pyarrow as pa

writer = None
for chunk in ...:
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema)
    writer.write_table(table)
writer.close()
```

## Satır grubu büyüklüğü (bir milyon sipariş, bu bilgisayarda)

| `row_group_size` | Grup | Dosya | Okuma |
|---|---|---|---|
| 1 000 | 1 000 | 27,1 MB | 0,121 sn |
| 10 000 | 100 | 27,1 MB | 0,049 sn |
| 100 000 | 10 | 26,0 MB | 0,037 sn |
| 1 000 000 | 1 | 20,9 MB | 0,057 sn |

Çok küçük gruplar okumayı yavaşlatıyor (her grubun kendi hazırlığı var). Tek
dev grup en küçük dosyayı veriyor ama atlanacak hiçbir şey bırakmıyor. Arada
bir yer (on binlerce – yüz binlerce satır) çoğu zaman iyi.
