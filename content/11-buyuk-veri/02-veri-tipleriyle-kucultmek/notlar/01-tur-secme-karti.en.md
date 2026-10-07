Follow the order on this page to choose which type to give a column.

## Which type for which column?

| What is in the column? | Type | Per row |
|---|---|---|
| Small whole numbers (−128 … 127) | `int8` | 1 byte |
| Small numbers that are never negative (0 … 255) | `uint8` | 1 byte |
| Medium whole numbers (±32 767) | `int16` | 2 bytes |
| Large whole numbers (±2.1 billion) | `int32` | 4 bytes |
| Larger still | `int64` | 8 bytes |
| Whole numbers with missing values | `Int8` … `Int64` | 2 … 9 bytes |
| Decimals, 7 digits are enough | `float32` | 4 bytes |
| Decimals, money or precise arithmetic | `float64` | 8 bytes |
| Text with few different values (city, colour) | `category` | 1–2 bytes + list |
| Text where nearly every value differs (name, address) | `str` | text + 8 bytes |
| A date or time | `datetime64` | 8 bytes |
| Yes / no | `bool` | 1 byte |

## Checking

```python
df["col"].min(), df["col"].max()     # the range
df["col"].nunique()                  # number of different values
df["col"].isna().sum()               # number of missing values
np.iinfo("int16")                    # the type's range
```

## Converting

```python
df["quantity"] = df["quantity"].astype("int8")
df["customer_id"] = pd.to_numeric(df["customer_id"], downcast="integer")
df["city"] = df["city"].astype("category")
df["order_time"] = pd.to_datetime(df["order_time"])

df = df.astype({"order_id": "int32", "payment": "category"})
```

## Giving them while reading (best)

```python
df = pd.read_csv(
    "orders.csv",
    dtype={"order_id": "int32", "customer_id": "int32", "quantity": "int8",
           "unit_price": "float32", "city": "category",
           "category": "category", "payment": "category"},
    parse_dates=["order_time"],
)
```

## This track's result (1 million orders)

| Column | Before | After |
|---|---|---|
| `order_id` | `int64`, 7.6 MB | `int32`, 3.8 MB |
| `order_time` | `str`, 25.8 MB | `datetime64`, 7.6 MB |
| `customer_id` | `int64`, 7.6 MB | `int32`, 3.8 MB |
| `city` | `str`, 13.8 MB | `category`, 0.95 MB |
| `category` | `str`, 13.6 MB | `category`, 0.95 MB |
| `quantity` | `int64`, 7.6 MB | `int8`, 0.95 MB |
| `unit_price` | `float64`, 7.6 MB | `float32`, 3.8 MB |
| `payment` | `str`, 12.2 MB | `category`, 0.95 MB |
| **Total** | **95.9 MB** | **22.9 MB** |
