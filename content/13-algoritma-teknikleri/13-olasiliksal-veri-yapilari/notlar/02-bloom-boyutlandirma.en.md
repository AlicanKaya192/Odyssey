Before building a Bloom filter you need to know two things: how many items
(`n`) will come and which false positive rate (`p`) you accept. The number of
bits and the number of hashes needed follow from these:

- `m = −n · ln p / (ln 2)²` bits
- `k = (m / n) · ln 2` hashes

```python
import math


def bloom_size(n, p):
    m = math.ceil(-n * math.log(p) / math.log(2) ** 2)
    k = round(m / n * math.log(2))
    return m, k


for n, p in [(1_000_000, 0.01), (1_000_000, 0.001), (100_000_000, 0.01)]:
    m, k = bloom_size(n, p)
    print(n, p, round(m / 8 / 1_000_000, 1), "MB", k, "hashes")
```

```text
1000000 0.01 1.2 MB 7 hashes
1000000 0.001 1.8 MB 10 hashes
100000000 0.01 119.8 MB 7 hashes
```

For a million items a 1% error takes 1.2 MB; cutting the error tenfold raises
memory only about 1.5 times. About 10 bits per item are enough for a 1% error,
and this is **independent** of how long the items are: keeping a million long
addresses in a set would take more than a hundred megabytes.

In the lesson we chose `n = 10,000`, `m = 100,000` (10 bits per item) and
`k = 7`: the same values the formula suggests.
