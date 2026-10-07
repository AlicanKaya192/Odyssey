Compare how much of the year `head` and a random sample cover.

**What to do:**

1. `orders = make_orders(200_000)`; turn `order_time` into a date.
2. Prepare two samples: `orders.head(5_000)` and
   `orders.sample(n=5_000, random_state=0)`.
3. For each, print on one line its name (`head` / `random`), the number of
   different months it covers and the earliest and latest date (`.date()`).
4. For each, print the number of different days it covers
   (`order_time.dt.date.nunique()`) on a line, first `head`, then
   `random`.

**Expected output:**

```
head 1 2024-01-01 2024-01-10
random 12 2024-01-01 2024-12-31
head 10
random 366
```

`head` saw only the first days of January.
