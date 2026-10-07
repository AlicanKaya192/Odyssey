Do the same calculation two ways and measure the peak memory with
`tracemalloc`.

The calculation: add 20% tax to each of 2 million prices and round the result
to two decimals.

**What to do:**

1. **First way** (a new array at every step):
   - `tracemalloc.start()`
   - `prices = np.ones(2_000_000)`
   - `taxed = prices * 1.2`
   - `final = np.round(taxed, 2)`
   - Take the peak, `tracemalloc.stop()`.
2. **Second way** (on the same array, *in place*):
   - `tracemalloc.start()`
   - `prices = np.ones(2_000_000)`
   - `prices *= 1.2`
   - `np.round(prices, 2, out=prices)`
   - Take the peak, `tracemalloc.stop()`.
3. Print the two peaks in MB, rounded to one decimal, on separate lines.
4. On the last line print the ratio of the first peak to the second, rounded
   to a whole number.

`prices *= 1.2` changes the array on top of itself without building a new
one; `out=prices` says the result should be written into the same array.

**Expected output:**

```
45.8
15.3
3
```

The result is the same, but the first way holds three arrays in memory at
once.
