How unbalanced is the load when orders are spread over three reduce
machines by city?

**What to do:**

1. Write the function `partition(key, reducers)` with `zlib.crc32`.
2. `orders = make_orders(200_000)`; assign each order's city to a machine
   with `partition(city, 3)`.
3. Print the number of orders each machine gets, as a list sorted by machine
   number.
4. Print each machine's share as a percentage (one decimal), as a list.
5. Print the ratio of the busiest machine to the least busy one (one
   decimal).

**Expected output:**

```
[132175, 57962, 9863]
[66.1, 29.0, 4.9]
13.4
```

One machine gets more than ten times the work of another: the job will finish
only when the slowest machine finishes.
