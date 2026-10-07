Bölümlenmiş veriyi yazmak, okumak ve klasörlerde gezinmek için gereken
satırlar.

## Düzen

```text
orders/
  month=2024-01/part-0.parquet
  month=2024-02/part-0.parquet
  ...
```

Klasör adı `sütun=değer`. Bölüm sütunu dosyanın içinde değil, adında.

## Elle yazmak

```python
from pathlib import Path

for month, part in df.groupby("month"):
    folder = Path("orders") / f"month={month}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="month").to_parquet(folder / "part-0.parquet", index=False)
```

## Elle okumak

```python
parts = []
for f in sorted(Path("orders").glob("month=*/*.parquet")):
    month = f.parent.name.split("=")[1]
    if month == "2024-03":                 # bölüm budama
        p = pd.read_parquet(f)
        p["month"] = month                 # sütunu adından geri koy
        parts.append(p)
result = pd.concat(parts, ignore_index=True)
```

## pandas'a bıraktırmak

```python
df.to_parquet("by_month", partition_cols=["month"], index=False)
pd.read_parquet("by_month")
pd.read_parquet("by_month", filters=[("month", "==", "2024-03")])
```

Arkada `pyarrow.dataset` gerekiyor; yoksa elle yöntem.

## `pathlib` ile klasörler

| Kod | Ne yapar |
|---|---|
| `Path("orders") / "month=2024-03"` | Yol birleştirir |
| `folder.mkdir(parents=True, exist_ok=True)` | Klasörü açar; varsa hata vermez |
| `Path("orders").glob("month=*/*.parquet")` | Bir alt düzeydeki Parquet dosyaları |
| `Path("orders").rglob("*.parquet")` | Bütün alt klasörlerdeki Parquet dosyaları |
| `f.parent.name` | Dosyanın klasörünün adı |
| `f.name` | Dosyanın adı |
| `f.stat().st_size` | Dosyanın boyutu, bayt |
| `f.as_posix()` | Yolu `/` ile yazar |

## Kovalama

```python
df["bucket"] = df["customer_id"] % 8
for bucket, part in df.groupby("bucket"):
    ...
# 1234 numaralı müşteri: yalnızca 1234 % 8 = 2 numaralı kova okunur
```

## Bölüm sütunu seçmek

| Soru | İyi cevap |
|---|---|
| Sık süzülüyor mu? | Evet: zaman, ülke, kaynak |
| Kaç farklı değeri var? | Onlarca, en fazla birkaç bin |
| Bir bölüm ne kadar büyük olur? | Büyük sistemlerde onlarca – yüzlerce MB |

Bu patikanın ölçümü (bir milyon sipariş): aya göre 12 dosya iyi; güne göre
366 dosya, hepsini okumak tek dosyadan on beş kat yavaş.
