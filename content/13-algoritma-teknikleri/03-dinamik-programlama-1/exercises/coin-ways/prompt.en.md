Write the function `count_ways(amount, coins)`: it returns **in how many
different ways** the amount can be given with the coins. Order does not
matter: `2 + 5` and `5 + 2` are the same.

`ways = [1] + [0] * amount`; **the outer loop is the coins**, the inner loop
the amounts: `ways[a] += ways[a − c]`.

**Expected output:**

```
10
292
321335886
```
