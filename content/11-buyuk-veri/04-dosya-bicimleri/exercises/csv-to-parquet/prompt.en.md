Move a CSV file to Parquet together with its types and confirm that
nothing was lost.

**What to do:**

1. Write the CSV with `write_orders_csv("orders.csv", 300_000)`.
2. Read the CSV as `df` with these types: `city`, `category`, `payment` as
   `"category"`, `quantity` as `"int8"`, `order_time` as a date
   (`parse_dates`).
3. Write `df` as `orders.parquet` with `zstd` compression.
4. Print the CSV and Parquet sizes in MB (one decimal) on one line, and below
   it the CSV / Parquet ratio (one decimal).
5. Read the Parquet back as `back`. Print two things on one line:
   `back.equals(df)` and whether the types are the same
   (`(back.dtypes == df.dtypes).all()`).

**Expected output:**

```
18.0 4.7
3.9
True True
```

`True True`: both the values and the types are exactly the same; from now on
there is no need to give the types again whenever this file is read.
