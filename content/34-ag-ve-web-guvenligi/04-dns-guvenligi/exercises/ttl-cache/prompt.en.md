`queries` are `[t, name]` queries in time order.
`cache_results(queries, ttl)` should return a list of `"hit"` or `"miss"`
for each query. It is a hit if the name is in the cache and `t` is
**less** than its expiry time; otherwise it is a miss and the name is
written into the cache until time `t + ttl`. A hit does not extend the
cache.

**Expected output:**

```
0 example.com miss
100 example.com hit
150 www.example.com miss
300 example.com miss
449 www.example.com hit
450 www.example.com miss
```
