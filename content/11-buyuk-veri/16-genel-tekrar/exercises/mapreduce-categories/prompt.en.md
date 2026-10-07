Work out the revenue per category with MapReduce and a combiner on four
"machines".

**What to do:**

1. `orders` (100 000 rows) is ready split over four machines: `machines` is a
   list of four tables.
2. **Map + combiner:** on each machine, add up the `(category, revenue)` pairs
   inside the machine; each machine's result is a dictionary.
3. **Shuffle:** send every key to reducer number
   `zlib.crc32(key.encode()) % 2` (per reducer, key → list of values).
4. **Reduce:** add up each key's values.
5. Print: the number of pairs that crossed the network (with the combiner),
   each reducer's keys (in alphabetical order, with the reducer's number),
   and whether the results match pandas `groupby` within less than 0.01.

**Expected output:**

```
24
0 books electronics home sports
1 clothing toys
True
```
