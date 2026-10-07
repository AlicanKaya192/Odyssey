dask ile en sık yazacağın satırlar.

## Tablo kurmak

```python
import dask.dataframe as dd

ddf = dd.read_csv("orders-*.csv")                       # her dosya bir bölüm
ddf = dd.read_csv("big.csv", blocksize="64MB")          # büyük dosyayı böl
ddf = dd.read_parquet("orders.parquet", split_row_groups=True)
ddf = dd.from_pandas(df, npartitions=8)
```

## Bakmak

```python
ddf.npartitions          # bölüm sayısı
ddf.dtypes               # türler (okumadan)
ddf.head()               # ilk bölümün ilk satırları (hemen çalışır)
len(ddf)                 # bütün dosyaları sayar (hemen çalışır)
```

## Hesaplamak

```python
result = ddf.groupby("city")["unit_price"].mean()   # tarif
result.compute()                                     # pandas sonucu

import dask
a, b = dask.compute(x, y)                            # iki sonuç, ortak okuma
```

## Bölüm bölüm iş

```python
ddf.map_partitions(len).compute()                    # her bölümün satır sayısı
ddf.map_partitions(lambda p: p[p["quantity"] >= 4])  # her bölüme aynı işlem
```

## Zamanlayıcı

```python
result.compute(scheduler="threads")        # varsayılan (tablolar)
result.compute(scheduler="processes")      # saf Python ağırlıklı iş
result.compute(scheduler="synchronous")    # hata ayıklamak için
```

## `delayed`

```python
from dask import delayed

parts = [delayed(f)(i) for i in range(8)]
total = delayed(sum)(parts)
total.compute()
```

## `bag`

```python
import dask.bag as db

if __name__ == "__main__":                 # varsayılanı süreçler
    bag = db.read_text("orders.jsonl").map(json.loads)
    bag.filter(lambda r: r["city"] == "Izmir").count().compute()
    bag.pluck("payment").frequencies().compute()
```

## Bu patikanın ölçümleri

| İş | Süre |
|---|---|
| 4 CSV, şehir başına ciro, pandas | 1,41 sn |
| Aynı iş, dask `threads` | 0,98 sn |
| Aynı iş, dask `synchronous` | 1,45 sn |
| 8 × 0,2 sn bekleme, `delayed` | 0,21 sn |
| Aynısı sırayla | 1,61 sn |
