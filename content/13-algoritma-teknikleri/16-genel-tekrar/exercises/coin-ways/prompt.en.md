Write the function `coin_ways(amount, coins)` with **dynamic programming**: it
returns in how many different ways `amount` can be made using the coins as
many times as you like; order does not matter (`1 + 2` and `2 + 1` are the
same).

`ways[0] = 1`; for each coin `ways[t] += ways[t - c]`, with `t` from small to
large. The coins must be in the outer loop, otherwise orders are counted
separately.

**Expected output:**

```
4
0
234896541
```
