# Prefix Sums

If you will ask "what are the total sales from day 3 to day 6?" once, adding
them in a loop is enough. But if users on a dashboard ask thousands of
different ranges, adding from scratch for every question is `O(n)` each,
`O(n × questions)` in total. This section's technique prepares the list
**once** and then answers every range question **with a single
subtraction**: **prefix sums**.

## What is a prefix sum?

A list's prefix sum is the **running total** up to each position (a
cumulative sum). Putting a `0` at the front makes things easier:

```python
from itertools import accumulate

sales = [3, 1, 4, 1, 5, 9, 2, 6]
prefix = [0]
for x in sales:
    prefix.append(prefix[-1] + x)
print(prefix)
print(sum(sales[2:6]), prefix[6] - prefix[2])
print([0] + list(accumulate(sales)))
```

```text
[0, 3, 4, 8, 9, 14, 23, 25, 31]
19 19
[0, 3, 4, 8, 9, 14, 23, 25, 31]
```

`prefix[i]` is the sum of the first `i` elements. So the sum of the range
`sales[lo:hi]` is one line:

```text
sum(lo, hi) = prefix[hi] - prefix[lo]
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>sales</span><span><code>[3, 1, 4, 1, 5, 9, 2, 6]</code></span></div>
    <div class="anat-row"><span>prefix</span><span><code>[0, 3, 4, 8, 9, 14, 23, 25, 31]</code></span></div>
    <div class="anat-row"><span>sales[2:6] = 4 + 1 + 5 + 9</span><span><code>prefix[6] - prefix[2]</code> = 23 − 4 = 19</span></div>
  </div>
  <figcaption>prefix[6] adds the first six days, prefix[2] the first two; their difference is the four days in between.</figcaption>
</figure>

`itertools.accumulate` gives the same running total ready-made; `cumsum()` in
pandas and `np.cumsum()` in NumPy are the equivalents.

## How much does it save?

We answered 2 000 range questions on a list of 100 000 elements in two ways
and counted the steps:

```text
from scratch: 99882591
prefix sums : 102000
```

Adding from scratch is about 100 million steps; the prefix sum was built once
(100 000 steps) and answered every question with a single subtraction.
**Preparation `O(n)`, each question `O(1)`.** If many questions will be asked
of the same data, this pattern pays.

## Counting the pieces that add up to k

A harder question: how many **consecutive pieces** of the list add up to
exactly `k`? If the numbers can be negative, the previous section's sliding
window does not work (shrinking the window can raise the sum).

Let us think with prefix sums: the piece between `lo` and `hi` sums to
`prefix[hi] - prefix[lo]`. For that to be `k`, we need
`prefix[lo] = prefix[hi] - k`. So while walking the list we ask, at each
position, **how many times the value `prefix - k` has been seen so far**. A
dictionary keeps those counts:

```python
def count_sum_k(values, k):
    seen = {0: 1}          # the empty prefix: sum 0, once
    total = 0
    count = 0
    for x in values:
        total += x                         # the current prefix sum
        count += seen.get(total - k, 0)    # matching pieces ending here
        seen[total] = seen.get(total, 0) + 1
    return count
```

Let us compare with brute force (trying every piece); the lines are
`(number of pieces, steps)`:

```text
(4, 21)
(4, 6)
(21594, 4501500) (21594, 3000)
```

The first two lines are the small example (`[1, 2, -1, 3, -2, 2]`, `k = 3`):
both methods found 4 pieces. On the last line, on a list of 3000 numbers,
the two methods gave the same result; brute force took 4.5 million steps, the
prefix sum 3000. This pattern (**prefix sum + dictionary**) is very powerful in
data work: questions like "the period with this total", "a range whose mean
is zero", "a piece with as many 0s as 1s" all reduce to it.

## The reverse operation: the difference array

The prefix sum was for "many questions, unchanging data". There is the
reverse too: **many updates**. Applying range updates like "add 3 to every
day from day 1 to day 4" one by one takes `O(range)` each. A **difference
array** records each update in two steps: `+amount` at the start of the range,
`−amount` one past its end. At the end, one prefix sum gives each day's real
value.

```python
def apply_updates(n, updates):
    diff = [0] * (n + 1)
    for lo, hi, amount in updates:     # lo..hi inclusive
        diff[lo] += amount
        diff[hi + 1] -= amount
    result = []
    running = 0
    for i in range(n):
        running += diff[i]             # the prefix sum
        result.append(running)
    return result

print(apply_updates(6, [(0, 2, 5), (1, 4, 3), (3, 5, -1)]))
```

```text
[5, 8, 8, 2, 2, -1]
```

Day 0: only +5. Days 1–2: +5 and +3. Days 3–4: +3 and −1. Day 5: only −1.
`O(u + n)` for `u` updates and `n` days.

## Summary

- Prefix sum: `prefix[i]` is the sum of the first `i` elements; put a `0` at
  the front.
- Range sum `prefix[hi] - prefix[lo]`: preparation `O(n)`, question `O(1)`.
- Ready-made: `itertools.accumulate`, `pandas.cumsum`, `np.cumsum`.
- Counting pieces adding up to `k`: prefix sum + dictionary, `O(n)` even with
  negative numbers.
- Difference array: record range updates in `O(1)`, apply them at the end with
  one prefix sum.
