# Probabilistic Data Structures

Keeping exactly which of billions of users visited the site before, how many
**distinct** IP addresses arrived in a day or which words are searched most
requires storing every item. Memory is not enough. **Probabilistic data
structures** accept a small and **measurable** margin of error and shrink
memory hundreds of times. They all rest on the same tool: a **hash function**
that turns an item into a random-looking number.

## Seeded hash

We want many numbers from one item that look independent of each other.
Combining the item with a seed and hashing is enough; `hashlib` gives the same
result on every computer and every run (Python's `hash()` does not).

```python
import hashlib
import math
import sys


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


print(h("data", 0), h("data", 0) == h("data", 0), h("data", 1) == h("data", 0))
```

```text
6802316569817657998 True False
```

The same item and the same seed always give the same 64-bit number; a
different seed gives a completely different number.

## Bloom filter: "definitely not" or "probably yes"

A **Bloom filter** is an array of `m` bits and `k` hash functions. Adding an
item: set the bits pointed to by the `k` hashes to 1. A query: if **all** `k`
bits are 1, "probably yes"; if even one is 0, "definitely not".

<figure class="fig">
<svg viewBox="0 0 682 66" width="682" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">bits</text>
<text class="dim" x="89.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="38" height="36"/>
<text class="ink" x="89.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="127.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="108" y="26" width="38" height="36"/>
<text class="ink" x="127.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="165.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="146" y="26" width="38" height="36"/>
<text class="ink" x="165.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="203.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="184" y="26" width="38" height="36"/>
<rect class="curve4" x="186" y="28" width="34" height="32" rx="4"/>
<text class="ink" x="203.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="241.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="222" y="26" width="38" height="36"/>
<text class="ink" x="241.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="279.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="260" y="26" width="38" height="36"/>
<text class="ink" x="279.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="317.0" y="18" font-size="12" text-anchor="middle">6</text>
<rect class="box" x="298" y="26" width="38" height="36"/>
<text class="ink" x="317.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="355.0" y="18" font-size="12" text-anchor="middle">7</text>
<rect class="box" x="336" y="26" width="38" height="36"/>
<text class="ink" x="355.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="393.0" y="18" font-size="12" text-anchor="middle">8</text>
<rect class="box" x="374" y="26" width="38" height="36"/>
<text class="ink" x="393.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="431.0" y="18" font-size="12" text-anchor="middle">9</text>
<rect class="box" x="412" y="26" width="38" height="36"/>
<rect class="curve4" x="414" y="28" width="34" height="32" rx="4"/>
<text class="ink" x="431.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="469.0" y="18" font-size="12" text-anchor="middle">10</text>
<rect class="box" x="450" y="26" width="38" height="36"/>
<rect class="curve4" x="452" y="28" width="34" height="32" rx="4"/>
<text class="ink" x="469.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="507.0" y="18" font-size="12" text-anchor="middle">11</text>
<rect class="box" x="488" y="26" width="38" height="36"/>
<text class="ink" x="507.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="545.0" y="18" font-size="12" text-anchor="middle">12</text>
<rect class="box" x="526" y="26" width="38" height="36"/>
<text class="ink" x="545.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="583.0" y="18" font-size="12" text-anchor="middle">13</text>
<rect class="box" x="564" y="26" width="38" height="36"/>
<text class="ink" x="583.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="621.0" y="18" font-size="12" text-anchor="middle">14</text>
<rect class="box" x="602" y="26" width="38" height="36"/>
<text class="ink" x="621.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="659.0" y="18" font-size="12" text-anchor="middle">15</text>
<rect class="box" x="640" y="26" width="38" height="36"/>
<text class="ink" x="659.0" y="48.9" font-size="14" text-anchor="middle">0</text>
</svg>
<figcaption>16 bits, 3 hashes. <code>cat</code> set bits [1, 4, 14] and <code>dog</code> [9, 10, 14] to 1. <code>fox</code> looks at the green-ringed bits [3, 9, 10]; one is 0, so it is definitely absent.</figcaption>
</figure>

```python
class Bloom:
    def __init__(self, bits, hashes):
        self.bits = bytearray(bits)            # one byte per bit, for simplicity
        self.hashes = hashes

    def _spots(self, item):
        return [h(item, s) % len(self.bits) for s in range(self.hashes)]

    def add(self, item):
        for i in self._spots(item):
            self.bits[i] = 1

    def __contains__(self, item):
        return all(self.bits[i] for i in self._spots(item))


bloom = Bloom(100_000, 7)
seen = [f"user{i}" for i in range(10_000)]
for name in seen:
    bloom.add(name)
print(all(name in bloom for name in seen))
false_hits = sum(f"guest{i}" in bloom for i in range(10_000))
expected = (1 - math.exp(-7 * 10_000 / 100_000)) ** 7      # the formula
print(false_hits / 10_000, round(expected, 4))
set_bytes = sys.getsizeof(set(seen)) + sum(sys.getsizeof(s) for s in seen)
print(sys.getsizeof(bloom.bits), set_bytes)
```

```text
6802316569817657998 True False
True
0.0073 0.0082
100057 1013394
```

All ten thousand added names were found: a Bloom filter **gives no false
negatives**. Of ten thousand names never added, 73 got "probably yes": a false
positive rate of 0.73%, close to the 0.82% the formula predicts. Memory: this
simple version uses a byte per bit and takes about 100 KB; with packed bits it
would be 12.5 KB. Keeping the same names in a set takes about 1 MB.

A Bloom filter stands at the door before an expensive job: a database asks
"is this key definitely absent?" before going to disk (Cassandra and LevelDB
work this way).

## Count-Min sketch: roughly how many times?

Counting how many times each item occurs in a stream needs a counter per item.
A **Count-Min sketch** is a table of counters with `d` rows and `w` columns.
Each row has its own hash; when an item arrives, one counter goes up in every
row. The estimate is the **smallest** of the item's `d` counters: other items
can land on the same counter and inflate it, but no counter can fall below the
true count.

```python
import random
from collections import Counter

random.seed(4)
words = ["the", "data", "model", "train", "test", "loss", "batch", "epoch"]
weights = [400, 200, 100, 60, 40, 20, 10, 5]
stream = random.choices(words, weights=weights, k=20_000)
stream += [f"rare{i}" for i in range(3000)]


class CountMin:
    def __init__(self, width, depth):
        self.table = [[0] * width for _ in range(depth)]

    def add(self, item):
        for row, counts in enumerate(self.table):
            counts[h(item, row) % len(counts)] += 1

    def estimate(self, item):
        return min(counts[h(item, row) % len(counts)]
                   for row, counts in enumerate(self.table))


cms = CountMin(200, 4)
for w in stream:
    cms.add(w)
true = Counter(stream)
for w in ["the", "batch", "epoch", "rare7"]:
    print(w, true[w], cms.estimate(w))
```

```text
6802316569817657998 True False
the 9678 9693
batch 244 258
epoch 130 140
rare7 1 11
```

800 counters for 3008 distinct items. For frequent items the estimate is very
close to the truth (`the`: 9693 instead of 9678); `rare7`, seen once, shows up
as 11. Count-Min always **overestimates**, and the error does not matter for
frequent items: tailor-made for the "most searched" (heavy hitters) question.

## HyperLogLog: how many distinct items?

For the number of distinct items (cardinality), look at the leading zeros in a
hash's binary form. Half of the hashes start with `1`, a quarter with `01`, an
eighth with `001`. If the longest run of zeros you have seen is `r`, you have
seen about `2ʳ` distinct items. Since a single estimate is very unsteady,
**HyperLogLog** spreads the items into `m` buckets by the hash's first bits,
each bucket keeps its own longest run, and a suitable average of the results is
taken.

```python
def hll_count(items, p=10):
    m = 1 << p                                 # 1024 buckets
    registers = [0] * m
    for item in items:
        v = h(item, 0)
        bucket = v & (m - 1)                   # the last p bits: the bucket
        rest = v >> p
        rank = (64 - p) - rest.bit_length() + 1   # leading zeros + 1
        registers[bucket] = max(registers[bucket], rank)
    alpha = 0.7213 / (1 + 1.079 / m)
    estimate = alpha * m * m / sum(2.0 ** -r for r in registers)
    zeros = registers.count(0)
    if estimate <= 2.5 * m and zeros:          # correction for small counts
        estimate = m * math.log(m / zeros)
    return round(estimate)


for n in (1000, 50_000, 200_000):
    items = [f"id{i % n}" for i in range(3 * n)]   # each item three times
    est = hll_count(items)
    print(n, est, round(abs(est - n) / n * 100, 1))
```

```text
6802316569817657998 True False
1000 991 0.9
50000 48634 2.7
200000 192751 3.6
```

On every line each item occurs three times, but the distinct count is what is
counted. With 1024 small counters the error stays below 4% up to two hundred
thousand; the theoretical error is `1.04/√m` ≈ 3.3%. The memory stays the same
even when the items reach billions. Redis, BigQuery and Spark's
`approx_count_distinct` use this structure.

## MinHash: how similar are the sets?

The Jaccard similarity of two sets (common / union) needs the whole sets.
**MinHash** reduces each set to a **signature** of `k` numbers: for each seed,
the **smallest** of the hashes of the set's items. The probability that two
sets have the same smallest hash is exactly their Jaccard similarity; how many
of the `k` signatures agree estimates it.

```python
def shingles(text, k=3):
    w = text.split()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}


def signature(items, size=128):
    return [min(h(x, s) for x in items) for s in range(size)]


a = shingles("the quick brown fox jumps over the lazy dog "
             "near the river bank today")
b = shingles("the quick brown fox leaps over the lazy dog "
             "near the river bank today")
true_j = len(a & b) / len(a | b)
sa, sb = signature(a), signature(b)
est_j = sum(x == y for x, y in zip(sa, sb)) / len(sa)
print(round(true_j, 3), round(est_j, 3))
```

```text
6802316569817657998 True False
0.6 0.57
```

The true similarity is 0.6, the estimate with 128-number signatures 0.57.
Because signatures are small and of fixed size, millions of documents can be
compared; LSH (locality-sensitive hashing) splits the signatures into buckets
and compares only the candidates that land in the same bucket. Removing copied
documents from language models' training data is often done this way.

## Summary

| Structure | Question | Error | Memory |
|---|---|---|---|
| Bloom filter | is it there? | false positives, no false negatives | a few bits per item |
| Count-Min | how many times? | only overestimates | `w × d` counters |
| HyperLogLog | how many distinct? | `1.04/√m` | `m` small counters |
| MinHash | how similar? | shrinks as `k` grows | `k` numbers per set |
