For each of the four text columns, decide by measuring whether `category`
helps.

**What to do:**

1. Build the table `df` with `make_orders(100_000)`.
2. Loop over the `order_time`, `city`, `category` and `payment` columns.
3. For each column print on one line:
   - the number of different values (`nunique()`),
   - its kilobytes as `str`,
   - its kilobytes as `category`,
   - `yes` if `category` is smaller, otherwise `no`.
   Kilobytes are `memory_usage(deep=True) / 1024`, one decimal.

**Expected output:**

```
order_time 99830 2636.8 3035.2 no
city 8 1412.8 97.9 yes
category 6 1393.5 97.9 yes
payment 3 1249.7 97.8 yes
```

In three columns the size drops below a tenth; in `order_time`, where nearly
every value is different, the category is more expensive.
