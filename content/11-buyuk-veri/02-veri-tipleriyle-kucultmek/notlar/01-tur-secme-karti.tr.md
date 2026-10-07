Bir sütuna hangi türü vereceğini seçmek için bu sayfadaki sırayı izle.

## Hangi sütuna hangi tür?

| Sütunda ne var? | Tür | Satır başına |
|---|---|---|
| Küçük tam sayı (−128 … 127) | `int8` | 1 bayt |
| Hiç eksi olmayan küçük sayı (0 … 255) | `uint8` | 1 bayt |
| Orta tam sayı (±32 767) | `int16` | 2 bayt |
| Büyük tam sayı (±2,1 milyar) | `int32` | 4 bayt |
| Daha büyüğü | `int64` | 8 bayt |
| Eksik değerli tam sayı | `Int8` … `Int64` | 2 … 9 bayt |
| Ondalıklı, 7 basamak yeterli | `float32` | 4 bayt |
| Ondalıklı, para ya da hassas hesap | `float64` | 8 bayt |
| Az sayıda farklı metin (şehir, renk) | `category` | 1–2 bayt + liste |
| Neredeyse hepsi farklı metin (ad, adres) | `str` | metin + 8 bayt |
| Tarih ya da saat | `datetime64` | 8 bayt |
| Evet / hayır | `bool` | 1 bayt |

## Kontrol etmek

```python
df["col"].min(), df["col"].max()     # aralık
df["col"].nunique()                  # farklı değer sayısı
df["col"].isna().sum()               # eksik değer sayısı
np.iinfo("int16")                    # türün aralığı
```

## Dönüştürmek

```python
df["quantity"] = df["quantity"].astype("int8")
df["customer_id"] = pd.to_numeric(df["customer_id"], downcast="integer")
df["city"] = df["city"].astype("category")
df["order_time"] = pd.to_datetime(df["order_time"])

df = df.astype({"order_id": "int32", "payment": "category"})
```

## Okurken vermek (en iyisi)

```python
df = pd.read_csv(
    "orders.csv",
    dtype={"order_id": "int32", "customer_id": "int32", "quantity": "int8",
           "unit_price": "float32", "city": "category",
           "category": "category", "payment": "category"},
    parse_dates=["order_time"],
)
```

## Bu patikanın sonucu (1 milyon sipariş)

| Sütun | Önce | Sonra |
|---|---|---|
| `order_id` | `int64`, 7,6 MB | `int32`, 3,8 MB |
| `order_time` | `str`, 25,8 MB | `datetime64`, 7,6 MB |
| `customer_id` | `int64`, 7,6 MB | `int32`, 3,8 MB |
| `city` | `str`, 13,8 MB | `category`, 0,95 MB |
| `category` | `str`, 13,6 MB | `category`, 0,95 MB |
| `quantity` | `int64`, 7,6 MB | `int8`, 0,95 MB |
| `unit_price` | `float64`, 7,6 MB | `float32`, 3,8 MB |
| `payment` | `str`, 12,2 MB | `category`, 0,95 MB |
| **Toplam** | **95,9 MB** | **22,9 MB** |
