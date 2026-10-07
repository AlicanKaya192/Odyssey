Estimate Trabzon's mean price with a simple and a stratified sample.

**What to do:**

1. `orders = make_orders(200_000)`; work out Trabzon's real mean
   `unit_price`.
2. Repeat 50 times with `random_state` from 0 to 49:
   - a simple sample: `orders.sample(n=800, random_state=i)`,
   - a stratified sample: 100 orders from each city,
     `orders.groupby("city", group_keys=False).sample(n=100, random_state=i)`,
   - in each, add the absolute difference between the Trabzon mean estimate
     and the real value to that method's list.
3. For each method print on one line its name (`simple` / `stratified`) and
   the mean of its 50 differences (one decimal).

**Expected output:**

```
simple 100.8
stratified 57.5
```

In a single sample the stratified method can come out worse by chance; on
average Trabzon's error shrinks.
