# Greedy Algorithms

A **greedy** algorithm picks **what looks best right now** at each step and
never goes back. Backtracking tried every path; the greedy method walks a
single one. That makes it very fast and easy to write. But the price is
high: it does not give the right result on every problem. This section has
two questions:

1. Does the greedy choice **really** give the best on this problem?
2. If not, how bad is it?

## Making change

You have to give 87 cents in change; your coins are 1, 5, 10, 25 and 50
cents. The first idea for the fewest coins: always give the **largest** coin
that fits.

```python
def greedy_change(amount, coins):
    used = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            used.append(coin)
    return used

print(greedy_change(87, [1, 5, 10, 25, 50]))
print(greedy_change(6, [1, 3, 4]))
```

```text
[50, 25, 10, 1, 1]
[4, 1, 1]
```

Five coins in the first system, and that really is the fewest. In the second
system the greedy way gave **three** coins, `4 + 1 + 1`; yet `3 + 3` is
**two**. Taking the largest (4) in the first step put the next steps in a bad
position. Coin systems are usually designed so that greedy works; finding the
fewest in an arbitrary system needs the **dynamic programming** of the next
section.

## Choosing meetings

There is a single meeting room and many meeting requests came in for the day.
Two overlapping meetings cannot be held at the same time. We want to fit **as
many** meetings as possible. Three greedy rules come to mind:

- **Earliest start first:** take the meeting that starts first in the
  morning.
- **Shortest first:** take the one that keeps the room busy the least.
- **Earliest end first:** take the one that frees the room the earliest.

Every rule works the same way: sort the meetings by that rule, look at them in
order, take one if it does not overlap the chosen ones.

Which one is right? Two small counterexamples and the average over 200 random
days:

```python
def pick(meetings, key):
    chosen = []
    for start, end in sorted(meetings, key=key):
        if all(end <= s or start >= e for s, e in chosen):   # no overlap
            chosen.append((start, end))
    return len(chosen)

by_end = lambda m: m[1]
by_start = lambda m: m[0]
by_length = lambda m: m[1] - m[0]

for day in ([(9, 17), (10, 11), (11, 12), (12, 13)], [(1, 5), (4, 7), (6, 10)]):
    print(pick(day, by_end), pick(day, by_start), pick(day, by_length))
```

```text
3 1 3
2 2 1
```

```text
average over 200 days, 40 requests each
earliest end first  : 9.665
earliest start first: 6.285
shortest first      : 9.515
days another rule beat earliest end: 0
```

**Earliest start first** got stuck on the single meeting from 9 in the morning
to 5 in the afternoon. **Shortest first** picked the short meeting in the
middle on the second day and missed the two long ones. **Earliest end first**
found the best on both days, and on none of the 200 random days could the
other two rules beat it.

Why is it right? Swap the first meeting of any best solution for the meeting
that ends earliest: since it ends earlier, it overlaps none of the rest and
the count does not drop. This **exchange argument** is the classic way to show
that greedy choices are correct. Since the earliest-ending one is chosen
first, the total work is the sort: `O(n log n)`.

## The knapsack: fractional and whole

Your bag carries 50 kilos. There are three items (value, weight): `(60, 10)`,
`(100, 20)`, `(120, 30)`. The greedy rule: start with the highest **value per
kilo**.

- In the **fractional** knapsack you can split an item (flour, gold dust).
  The greedy rule gives exactly the best.
- In the **whole (0/1)** knapsack an item goes in entirely or not at all. The
  same rule can be wrong.

```python
items = [(60, 10), (100, 20), (120, 30)]       # (value, weight)

def fractional(items, capacity):
    total = 0
    for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        take = min(weight, capacity)
        total += value * take / weight
        capacity -= take
    return total

def greedy_whole(items, capacity):
    total = 0
    for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if weight <= capacity:
            total += value
            capacity -= weight
    return total

print(fractional(items, 50), greedy_whole(items, 50))
```

```text
240.0 160
```

With whole items the greedy way found 160 (the first two items), yet the
second and third items together are worth 220. The right solution of the
whole knapsack is in dynamic programming too.

## Huffman coding

When storing a text as bits, instead of giving each letter 8 bits, giving
**frequent letters short codes and rare ones long codes** makes the text
smaller. Huffman's greedy algorithm from 1952 finds the best such code: at
each step **merge the two rarest groups**.

```python
import heapq
from collections import Counter

def huffman(text):
    counts = sorted(Counter(text).items())
    heap = [(n, i, {ch: ""}) for i, (ch, n) in enumerate(counts)]
    heapq.heapify(heap)
    order = len(heap)
    while len(heap) > 1:
        n1, _, left = heapq.heappop(heap)       # the two rarest groups
        n2, _, right = heapq.heappop(heap)
        merged = {ch: "0" + code for ch, code in left.items()}
        merged.update({ch: "1" + code for ch, code in right.items()})
        heapq.heappush(heap, (n1 + n2, order, merged))
        order += 1
    return heap[0][2]

text = "abracadabra"
codes = huffman(text)
print(sorted(codes.items()))
print(sum(len(codes[ch]) for ch in text), "bits instead of", 8 * len(text))
```

```text
[('a', '0'), ('b', '110'), ('c', '100'), ('d', '101'), ('r', '111')]
23 bits instead of 88
```

<figure class="fig">
<svg viewBox="0 0 549 244" width="549" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="204.7" y1="153.0" x2="146.7" y2="217.0"/>
<text class="dim" x="165.7" y="185.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="204.7" y1="153.0" x2="262.7" y2="217.0"/>
<text class="dim" x="243.7" y="185.0" font-size="12" text-anchor="start">1</text>
<line class="line" x1="436.7" y1="153.0" x2="378.7" y2="217.0"/>
<text class="dim" x="397.7" y="185.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="436.7" y1="153.0" x2="494.7" y2="217.0"/>
<text class="dim" x="475.7" y="185.0" font-size="12" text-anchor="start">1</text>
<line class="line" x1="320.7" y1="89.0" x2="204.7" y2="153.0"/>
<text class="dim" x="252.7" y="121.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="320.7" y1="89.0" x2="436.7" y2="153.0"/>
<text class="dim" x="388.7" y="121.0" font-size="12" text-anchor="start">1</text>
<line class="line" x1="88.7" y1="25.0" x2="30.7" y2="89.0"/>
<text class="dim" x="49.7" y="57.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="88.7" y1="25.0" x2="320.7" y2="89.0"/>
<text class="dim" x="214.7" y="57.0" font-size="12" text-anchor="start">1</text>
<rect class="box" x="6.0" y="72.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="6.0" y="72.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="30.7" y="93.9" font-size="14" text-anchor="middle">a: 5</text>
<circle class="box" cx="88.7" cy="25.0" r="17"/>
<text class="ink" x="88.7" y="29.9" font-size="14" text-anchor="middle">11</text>
<rect class="box" x="122.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="122.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="146.7" y="221.9" font-size="14" text-anchor="middle">c: 1</text>
<circle class="box" cx="204.7" cy="153.0" r="17"/>
<text class="ink" x="204.7" y="157.9" font-size="14" text-anchor="middle">2</text>
<rect class="box" x="238.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="238.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="262.7" y="221.9" font-size="14" text-anchor="middle">d: 1</text>
<circle class="box" cx="320.7" cy="89.0" r="17"/>
<text class="ink" x="320.7" y="93.9" font-size="14" text-anchor="middle">6</text>
<rect class="box" x="354.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="354.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="378.7" y="221.9" font-size="14" text-anchor="middle">b: 2</text>
<circle class="box" cx="436.7" cy="153.0" r="17"/>
<text class="ink" x="436.7" y="157.9" font-size="14" text-anchor="middle">4</text>
<rect class="box" x="470.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="470.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="494.7" y="221.9" font-size="14" text-anchor="middle">r: 2</text>
</svg>
<figcaption>The Huffman tree of abracadabra. The leaves hold a letter and its count; the 0s and 1s on the path from the root are that letter's code (b = 110).</figcaption>
</figure>

`a`, which appears five times, gets the one-bit `0`; `c` and `d`, which appear
once each, get three bits. No code is the start of another code (**the prefix
property**), so the bits can be written side by side without separators and
still read in only one way. This idea runs inside ZIP, PNG and MP3 files.
Because a heap is used, it is `O(k log k)` for `k` different letters.

## Greedy choices in data science

**Forward selection:** trying every subset of 30 features meant more than a
billion models (the Backtracking section). The greedy way: at each step add
the feature that **helps the model the most**. On artificial data with six
features (the real relation is in features 0, 2 and 4):

```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(300, 6))
y = 3 * X[:, 0] - 2 * X[:, 2] + 0.5 * X[:, 4] + rng.normal(scale=0.5, size=300)

def r2(cols):                                    # R² of a linear regression
    A = np.column_stack([X[:, cols], np.ones(len(y))])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    residual = y - A @ coef
    return 1 - (residual ** 2).sum() / ((y - y.mean()) ** 2).sum()

chosen = []
for step in range(3):
    best = max((c for c in range(6) if c not in chosen), key=lambda c: r2(chosen + [c]))
    chosen.append(best)
    print(step + 1, chosen, round(r2(chosen), 3))
```

```text
1 [0] 0.642
2 [0, 2] 0.965
3 [0, 2, 4] 0.981
```

The right three features in three steps, `6 + 5 + 4 = 15` models instead of
`2⁶ = 64`. But there is no guarantee: greedy selection can miss features that
look weak alone but are strong together with another.

**Decision trees** are greedy too: at each node they pick the best split **for
now** and do not think about the next splits. Finding the best tree is a very
hard problem; that is why greedy splitting is used, and it is usually good
enough.

## Summary

- Greedy: pick what looks best right now at each step, never go back; fast
  and simple.
- Its correctness needs a proof (the exchange argument); finding a
  counterexample is often easy.
- Where it works: choosing meetings (earliest end first), the fractional
  knapsack, Huffman, canonical coin systems.
- Where it fails: an arbitrary coin system, the whole (0/1) knapsack; the
  right answer is in dynamic programming.
- In data science: forward feature selection and decision tree splits are
  greedy.
