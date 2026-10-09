# Counting Sorts

In the previous section we saw that no algorithm that sorts by comparing can
do better than `n log n` in the worst case. That limit has a condition:
**comparing**. If we can put elements directly in their places by looking at
their values, without comparing them with each other, we can get down to
`O(n)`. For that the data needs a property: its values must lie in a **small
range** or be splittable into **digits**.

## Counting sort

Imagine sorting a class's exam scores (0–100). You do not need to compare
scores with each other: open 101 boxes, look at each score and put a tally
mark in its box. Then walk through the boxes from 0 to 100 and write each
score as many times as it has tally marks.

```python
def counting_sort(items, max_value):
    counts = [0] * (max_value + 1)      # one counter per value
    for x in items:
        counts[x] += 1
    print(counts)
    result = []
    for value, count in enumerate(counts):
        result.extend([value] * count)  # write the value as many times as counted
    return result

print(counting_sort([4, 1, 3, 4, 0, 1, 4], 4))
```

```text
[1, 2, 0, 1, 3]
[0, 1, 1, 3, 4, 4, 4]
```

The first line is the counters: one 0, two 1s, no 2, one 3, three 4s. Not a
single comparison was made.

**Cost:** go over the elements once (`n`), go over the counters once (`k`,
the size of the value range): `O(n + k)`. Extra memory `O(k)`.

Is it really fast? We sorted the ages (0–100) of a million people:

```text
same result  : True
counting_sort: 54 ms
sorted       : 107 ms
```

Counting sort written in Python turned out faster than `sorted` written in
C, and the results are the same. When the value range is small, not comparing
really pays.

## When does it not help?

If `k` is large, counting sort gets worse. With values between 0 and a
billion you need a billion counters: both memory and time become far larger
than `n`. Negative values need shifting (`x - min_value`), and decimal
numbers cannot be used directly.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Counting sort fits</h4>
      <p>Exam scores (0–100), ages, months (1–12), hours (0–23)</p>
      <p>The range <code>k</code> is small; <code>O(n + k)</code> ≈ <code>O(n)</code></p></div>
    <div class="no"><h4>Does not fit</h4>
      <p>Salaries, populations, ID numbers, decimal measurements</p>
      <p>The range is huge or the values are not integers; use comparison sorting</p></div>
  </div>
  <figcaption>The deciding question: is the number of different values small compared with the number of elements?</figcaption>
</figure>

## Radix sort: digit by digit

If the values are large but can be split into **digits** (phone numbers,
postcodes, dates), **radix sort** helps. The idea: sort first by the **ones**
digit, then the **tens**, then the **hundreds**. In each round distribute into
10 buckets (0–9) and collect the buckets in order.

```python
def radix_sort(items):
    place = 1
    largest = max(items)
    while largest // place > 0:
        buckets = [[] for _ in range(10)]
        for x in items:
            buckets[(x // place) % 10].append(x)   # the digit at that place
        items = [x for bucket in buckets for x in bucket]
        print(place, items)
        place *= 10
    return items

radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
```

```text
1 [170, 90, 802, 2, 24, 45, 75, 66]
10 [802, 2, 24, 45, 66, 170, 75, 90]
100 [2, 24, 45, 66, 75, 90, 170, 802]
```

After the first round the list is sorted only by the last digit (170, 90,
802, 2…). After the third round it is fully sorted. Why does it work? Because
every round is **stable**: elements falling into the same bucket keep their
previous order. 24 and 45, with equal hundreds digits, stay side by side in
the order the first two rounds built. If the buckets were not stable, the
earlier rounds' work would be undone.

**Cost:** `d` digits, `n` elements and 10 buckets per round:
`O(d × (n + 10))`. If the number of digits is fixed (a 6-digit postcode,
say), `O(n)`.

## Bucket sort

If the values are **spread evenly** over a range (random numbers between 0
and 1, say), you split the range into `n` buckets and drop each number into
its bucket; each bucket holds one or two elements on average, you sort them
with a simple sort and join the buckets. `O(n)` on average. If the data piles
up in one bucket, the advantage is lost.

## Grouping with buckets: more important than sorting

The real idea of counting sort, using the value directly as an **address**, is
useful well beyond sorting:

- **Histogram:** how many of each value? (the `counts` list itself)
- **Grouping:** listing the students with the same grade together
  (`buckets[grade].append(name)`)
- **The k-th largest:** walk the counters from largest to smallest and stop
  when you reach `k`; no need to sort the whole list.

## Summary

- Sorting without comparing gets below the `n log n` limit.
- Counting sort: `O(n + k)` if the value range `k` is small; not used when
  `k` is large.
- Radix sort: digit by digit, with **stable** buckets in each round;
  `O(d × (n + base))`.
- Bucket sort: `O(n)` on average for evenly spread data.
- Using the value as an address (histograms, grouping) is common beyond
  sorting too.
