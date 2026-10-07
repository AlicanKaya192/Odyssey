Elinde bir CSV var ve onu Parquet'ye taşımak istiyorsun. Adımlar ve bu
makinede denenmiş tuzaklar.

## 1. Türleri bir kez doğru ver

```python
df = pd.read_csv(
    "orders.csv",
    dtype={"city": "category", "category": "category", "payment": "category",
           "quantity": "int8"},
    parse_dates=["order_time"],
)
df.to_parquet("orders.parquet", compression="zstd")
```

Parquet türleri sakladığı için bu iş **bir kez** yapılıyor. Bundan sonra
her `read_parquet` türleri hazır getiriyor.

## 2. Dosyanın içine bak

`pyarrow.parquet` dosyayı okumadan özetini veriyor:

```python
import pyarrow.parquet as pq

f = pq.ParquetFile("orders.parquet")
print(f.metadata.num_rows, f.metadata.num_columns, f.metadata.num_row_groups)
print(f.schema_arrow)
```

Satır sayısı, sütunlar ve türleri, satır grubu sayısı. Satır gruplarını
bir sonraki bölümde açacağız.

## 3. Yalnızca gerekeni oku

```python
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
```

## Tuzaklar

**`to_parquet` eklemiyor, baştan yazıyor.** Aynı dosyaya önce 100, sonra 50
satır yazınca dosyada 50 satır kaldı. Parça parça Parquet yazmak için ya her
parçayı ayrı dosyaya yaz (Bölüm 6) ya da `pyarrow.parquet.ParquetWriter`
kullan (Bölüm 5).

**İndeks saklanıyor.** `set_index("customer_id")` ile yazılan tablo geri
okununca indeksi yine `customer_id`; dosyada bu indeks bir sütun olarak
duruyor (`schema_arrow.names` listesinde sonda görünüyor). Varsayılan
`RangeIndex` ise yalnızca bir bilgi olarak saklanıyor, sütun açmıyor.

**İkili dosya.** Not Defteri'nde açılmıyor, gözle kontrol edilemiyor; içine
bakmak için yukarıdaki `pq.ParquetFile` ya da `pd.read_parquet(...).head()`.

**Kategoriler kategori olarak geri geliyor.** Parquet'den okunan
`category` sütunu yine `category`; kategori listesi dosyada saklanıyor.
