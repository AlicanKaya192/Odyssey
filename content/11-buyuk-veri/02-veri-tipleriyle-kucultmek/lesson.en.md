# Shrinking with Data Types

The last section's report said two things: the date is stored as text, and
the city, category and payment columns repeat the same few words. The
numeric columns also give every value 8 bytes, even though `quantity` never
goes above 5.

In this section we take the table of a million orders from 96 MB down to
23 MB by giving each column **the right type**. Not one row is deleted, not
one piece of information is lost. But choosing the wrong type has quiet traps
too; we will see those as well.

All the examples in the section start with the same table:

```python
import numpy as np
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
df = pd.read_csv("orders.csv")
```

## Whole numbers: choose the right width

pandas always turns the whole numbers in a CSV into `int64`: 8 bytes per
value, a range of about ±9 quintillion. For the number of items in a basket
that range is far too wide. Narrower types take less room:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>int8</code> · 1 byte</span><span>−128 … 127: counts, scores</span></div>
    <div class="anat-row"><span><code>int16</code> · 2 bytes</span><span>−32 768 … 32 767: years, small counters</span></div>
    <div class="anat-row"><span><code>int32</code> · 4 bytes</span><span>about ±2.1 billion: ID numbers</span></div>
    <div class="anat-row"><span><code>int64</code> · 8 bytes</span><span>about ±9.2 × 10¹⁸: the pandas default</span></div>
  </div>
  <figcaption>Each step is twice the room and a far wider range. Unsigned types with a <code>u</code> in front (<code>uint8</code>) hold no negatives and get twice the room on the positive side: 0 … 255.</figcaption>
</figure>

You can see each type's range with `np.iinfo`:

```python
for t in ["int8", "int16", "int32", "int64"]:
    i = np.iinfo(t)
    print(t, i.min, i.max)
```

```text
int8 -128 127
int16 -32768 32767
int32 -2147483648 2147483647
int64 -9223372036854775808 9223372036854775807
```

To choose the right type, first look at the column's **smallest and largest**
value:

```python
print(df["quantity"].min(), df["quantity"].max())
print(df["customer_id"].min(), df["customer_id"].max())
print(df["order_id"].min(), df["order_id"].max())
```

```text
1 5
1 249999
1 1000000
```

- `quantity` is between 1 and 5: `int8` (1 byte) is plenty.
- `customer_id` goes up to 249 999: above `int16`'s 32 767, so `int32`.
- `order_id` goes up to 1 000 000: `int32` again.

You change the type with `astype`:

```python
q8 = df["quantity"].astype("int8")
print(round(df["quantity"].memory_usage(deep=True) / 1024**2, 2))
print(round(q8.memory_usage(deep=True) / 1024**2, 2))
```

```text
7.63
0.95
```

The same column in an eighth of the room.

### `downcast`: letting pandas choose the type

Instead of looking at the range and choosing the type by hand, you can leave
it to pandas. `pd.to_numeric(..., downcast="integer")` picks the **smallest**
whole-number type the values fit into:

```python
print(pd.to_numeric(df["customer_id"], downcast="integer").dtype)
print(pd.to_numeric(df["order_id"], downcast="integer").dtype)
print(pd.to_numeric(df["quantity"], downcast="unsigned").dtype)
```

```text
int32
int32
uint8
```

`downcast="unsigned"` also tries **unsigned** types: `uint8` goes from 0 to
255 and holds no negative numbers. It suits values that are never negative,
such as counts, ages and counters.

## The trap: overflow

A small type has a price: a value outside its range can **break without any
error**.

```python
stock = pd.Series([100, 200, 300])
print(stock.astype("int8").tolist())
```

```text
[100, -56, 44]
```

200 and 300 went past `int8`'s limit of 127. pandas gave no warning; the
values wrapped around, like a clock hand going from 12 back to 1, and turned
into meaningless numbers. Arithmetic can overflow the same way:

```python
small = pd.Series([100, 120, 127]).astype("int8")
print((small + 1).tolist())
```

```text
[101, 121, -128]
```

<figure class="fig">
  <div class="flow">
    <span class="node">127<br><code>int8</code>'s limit</span><span class="arrow">→</span>
    <span class="node">+ 1</span><span class="arrow">→</span>
    <span class="node no">−128<br>wrapped around</span>
  </div>
  <figcaption>The value that overflows wraps around to the smallest value. pandas does not treat this as an error; the result is simply wrong.</figcaption>
</figure>

Three ways to protect yourself:

1. Look at `min()` and `max()` before changing the type.
2. Use `pd.to_numeric(..., downcast=...)` instead of `astype`; it does not
   force a value into a type it does not fit.
3. Leave room to grow. `quantity` is at most 5 today; if wholesale starts
   tomorrow it could be 300. If you are not sure, pick a type one step wider
   (`int16`).

## Decimal numbers: `float32`

`float64` has about 15–16 digits of precision and takes 8 bytes. `float32`
takes 4 bytes but holds only about **7 digits**:

```python
prices = pd.Series([19.99, 1234.56, 99999.99, 1234567.89])
print(prices.astype("float32").tolist())
```

```text
[19.989999771118164, 1234.56005859375, 99999.9921875, 1234567.875]
```

For small prices the difference is in the sixth decimal place; 1 234 567.89,
however, became 1 234 567.875. One by one it is small, but it grows when you
add up:

```python
p32 = df["unit_price"].astype("float32")
print(round(df["unit_price"].sum(), 2))
print(round(float(p32.sum()), 2))
print(round(float(p32.astype("float64").sum()), 2))
```

```text
736869041.37
736869056.0
736869041.4
```

Line 1: the real total (`float64`).
Line 2: the `float32` values added up in `float32`: off by 15 lira.
Line 3: the same `float32` values turned into `float64` and then added: the
error disappears.

The problem is not in the storing but in **adding up** with 7 digits. The
rules:

- `float32` is usually enough for measurements, ratios and model inputs.
- Turn it into `float64` when you add up or take an average.
- Do not use `float32` for **money**. A safer way: store cents as whole
  numbers (`(price * 100).round().astype("int64")`).

## Repeated text: `category`

The `city` column has a million rows but only 8 different cities. The
`category` type stores each different value **once** and keeps that value's
number in the rows:

<figure class="fig">
  <div class="versus">
    <div class="no"><h4><code>str</code></h4><p>The text itself in every row<br><code>"Istanbul"</code>, <code>"Trabzon"</code>, <code>"Istanbul"</code>, …<br>14.5 bytes per row</p></div>
    <div class="ok"><h4><code>category</code></h4><p>The list once: <code>Adana</code>, <code>Ankara</code>, … (8 cities)<br>A number in the rows: <code>4</code>, <code>7</code>, <code>4</code>, …<br>1 byte per row</p></div>
  </div>
  <figcaption>With few different values and many repeats, <code>category</code> is a big win. With many different values the list grows as long as the column and the win is gone.</figcaption>
</figure>

```python
city = df["city"].astype("category")
print(round(df["city"].memory_usage(deep=True) / 1024**2, 2))
print(round(city.memory_usage(deep=True) / 1024**2, 2))
print(city.cat.categories.tolist())
print(city.cat.codes.dtype, city.cat.codes.head(3).tolist())
```

```text
13.79
0.95
['Adana', 'Ankara', 'Antalya', 'Bursa', 'Istanbul', 'Izmir', 'Konya', 'Trabzon']
int8 [4, 7, 6]
```

- `cat.categories`: the list of different values (in alphabetical order).
- `cat.codes`: the number in each row. For 8 cities `int8` is enough: 1 byte
  per row. The first row is `4`, that is `Istanbul`.

The column went from 13.8 MB to 0.95 MB. But `category` is not right for
every text:

```python
print(df["order_time"].nunique())
t = df["order_time"].astype("category")
print(round(df["order_time"].memory_usage(deep=True) / 1024**2, 2))
print(round(t.memory_usage(deep=True) / 1024**2, 2))
```

```text
984369
25.75
29.28
```

There are 984 369 different times in a million rows; nearly all of them
appear once. Then the list of categories is as long as the column itself, and
the numbers come on top: the column **grew**. The rule:

> `category` helps when the number of different values is **small**
> compared with the number of rows. Check with `nunique()`.

A `category` column can be used like ordinary text: comparing with
`city == "Istanbul"`, `groupby("city")` and filtering all work as before.

## Dates: `datetime64`

`order_time` is really a date and time. As text it takes 27 bytes; as a date
type, 8 bytes:

```python
times = pd.to_datetime(df["order_time"])
print(times.dtype)
print(round(df["order_time"].memory_usage(deep=True) / 1024**2, 2))
print(round(times.memory_usage(deep=True) / 1024**2, 2))
```

```text
datetime64[us]
25.75
7.63
```

`datetime64[us]`: a date-time to the microsecond, 8 bytes. Three times
smaller, and now a real date: `times.dt.month` gives the month,
`times.dt.hour` the hour, and the difference between two dates can be worked
out.

## Missing values and "nullable" types

When a value is missing in a whole-number column, pandas quietly turns the
column into decimals, because `NaN` is a decimal number:

```python
s = pd.Series([1, 2, None, 4])
print(s.dtype, s.tolist())
n = pd.Series([1, 2, None, 4], dtype="Int8")
print(n.dtype, n.tolist())
```

```text
float64 [1.0, 2.0, nan, 4.0]
Int8 [1, 2, <NA>, 4]
```

The types written with a capital letter, `Int8`, `Int16`, `Int32` and
`Int64`, can hold a missing value as `<NA>`: 1 byte per value and 1 more byte
for "is this value missing?". For a small whole-number column with missing
values, much cheaper than `float64` (8 bytes).

Columns that hold `True` / `False` are of the `bool` type, 1 byte per value.

## All together

Let us give every column the right type:

```python
small = df.astype({
    "order_id": "int32",
    "customer_id": "int32",
    "quantity": "int8",
    "unit_price": "float32",
    "city": "category",
    "category": "category",
    "payment": "category",
})
small["order_time"] = pd.to_datetime(small["order_time"])
print(small.memory_usage(deep=True))
```

```text
Index              132
order_id       4000000
order_time     8000000
customer_id    4000000
city           1000113
category       1000087
quantity       1000000
unit_price     4000000
payment        1000041
dtype: int64
```

The total went from 95.9 MB down to **22.9 MB**: more than four times
smaller. The same rows, the same information.

`astype` can take a dictionary: `{"column": "type", ...}`. Columns not in the
dictionary stay as they are.

## Better still: shrinking while reading

Above, the table was first built at 96 MB, then shrunk. When memory is not
enough, even that first step may be impossible. `read_csv` can take the types
**while reading**:

```python
df = pd.read_csv(
    "orders.csv",
    dtype={"order_id": "int32", "customer_id": "int32", "quantity": "int8",
           "unit_price": "float32", "city": "category", "category": "category",
           "payment": "category"},
    parse_dates=["order_time"],
)
print(round(df.memory_usage(deep=True).sum() / 1024**2, 1))
```

```text
22.9
```

- `dtype=`: a dictionary of types per column.
- `parse_dates=`: the list of columns to read as dates.

The result is the same 22.9 MB, but you do not have to build the 96 MB table
first and shrink it afterwards.

## Decision table

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Whole numbers, small range</span><span><code>int8</code> / <code>int16</code> / <code>int32</code>; check <code>min</code>, <code>max</code> first</span></div>
    <div class="anat-row"><span>Whole numbers with missing values</span><span><code>Int8</code> … <code>Int64</code></span></div>
    <div class="anat-row"><span>Decimals, measurements</span><span><code>float32</code>; <code>float64</code> to add up</span></div>
    <div class="anat-row"><span>Money</span><span><code>float64</code>, or cents as whole numbers</span></div>
    <div class="anat-row"><span>Text, few different values</span><span><code>category</code></span></div>
    <div class="anat-row"><span>Text, mostly different</span><span>leave it as <code>str</code></span></div>
    <div class="anat-row"><span>Dates, times</span><span><code>datetime64</code> (<code>parse_dates</code>)</span></div>
  </div>
  <figcaption>Each row is a question: what is in the column? The answer chooses the type.</figcaption>
</figure>

## Summary

- pandas reads whole numbers as `int64` and decimals as `float64`. A
  narrower type that fits the values' range holds the same information in
  less room.
- `pd.to_numeric(..., downcast="integer")` picks the smallest safe type.
- **Overflow is silent:** `astype("int8")` turns 300 into 44. Check `min()` /
  `max()` first and leave room to grow.
- `float32` has about 7 digits; turn it into `float64` to add up, and do not
  use it for money.
- `category` is a big win for text with few different values (13.8 MB →
  0.95 MB) and a loss when nearly every value is different.
- Turn dates into `datetime64` with `pd.to_datetime`: 8 bytes instead of 27,
  plus date operations.
- For whole numbers with missing values, `Int8` … `Int64`.
- Best of all, give the types while reading: `read_csv(dtype=...,
  parse_dates=...)`. A million orders: 95.9 MB → 22.9 MB.
