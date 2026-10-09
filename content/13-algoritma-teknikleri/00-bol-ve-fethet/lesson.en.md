# Divide and Conquer

In ALG 1 you wrote merge sort and quick sort: split the list in two, solve
the two halves with yourself, combine the results. In this section we treat
the same idea as a **technique**: how the cost of a divide-and-conquer
algorithm is computed, when it helps, when it does not, and where it is used
beyond sorting.

<figure class="fig">
  <div class="flow">
    <span class="node">Divide<br><small>smaller pieces</small></span><span class="arrow">→</span>
    <span class="node acc">Conquer<br><small>solve each piece with yourself</small></span><span class="arrow">→</span>
    <span class="node ok">Combine<br><small>put the answers together</small></span>
  </div>
  <figcaption>If a piece is small enough (the base case) it is solved directly; otherwise the same three steps repeat inside the piece.</figcaption>
</figure>

## Computing the cost: the recursion tree

The cost of a divide-and-conquer algorithm depends on three numbers: **how
many pieces** the problem is split into, **how small** the pieces are, and
**how much work** splitting + combining takes. Drawing it as a tree makes
this easier. In merge sort each node does as much work as the size of its
piece (the merge):

<figure class="fig">
<svg viewBox="0 0 559 180" width="559" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="30" font-size="12">level 0: total n</text>
<text class="dim" x="4" y="94" font-size="12">level 1: total n</text>
<text class="dim" x="4" y="158" font-size="12">level 2: total n</text>
<line class="line" x1="198.8" y1="89.0" x2="136.8" y2="153.0"/>
<line class="line" x1="198.8" y1="89.0" x2="260.8" y2="153.0"/>
<line class="line" x1="446.8" y1="89.0" x2="384.8" y2="153.0"/>
<line class="line" x1="446.8" y1="89.0" x2="508.8" y2="153.0"/>
<line class="line" x1="322.8" y1="25.0" x2="198.8" y2="89.0"/>
<line class="line" x1="322.8" y1="25.0" x2="446.8" y2="89.0"/>
<rect class="box" x="116.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="136.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
<rect class="box" x="178.0" y="72.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="198.8" y="93.9" font-size="14" text-anchor="middle">n/2</text>
<rect class="box" x="240.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="260.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
<circle class="box" cx="322.8" cy="25.0" r="17"/>
<text class="ink" x="322.8" y="29.9" font-size="14" text-anchor="middle">n</text>
<rect class="box" x="364.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="384.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
<rect class="box" x="426.0" y="72.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="446.8" y="93.9" font-size="14" text-anchor="middle">n/2</text>
<rect class="box" x="488.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="508.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
</svg>
<figcaption>The recursion tree of merge sort. Each node does as much work as the size of its piece; every level adds up to n, and there are log₂ n levels.</figcaption>
</figure>

The pieces on each level still add up to `n`, so every level takes `n`
work. The number of levels is `log₂ n` (the pieces halve on every level).
Total: `n log n`.

Let us measure different shapes. The functions below compute nothing; they
only count **how much work** four different divide-and-conquer patterns do:

```python
def work_a(n):          # 2 pieces, combine n   (merge sort)
    if n <= 1:
        return 1
    return work_a(n // 2) + work_a(n - n // 2) + n

def work_b(n):          # 1 piece, combine n
    if n <= 1:
        return 1
    return work_b(n // 2) + n

def work_c(n):          # 1 piece, combine 1      (binary search)
    if n <= 1:
        return 1
    return work_c(n // 2) + 1

def work_d(n):          # 2 pieces, combine 1
    if n <= 1:
        return 1
    return work_d(n // 2) + work_d(n - n // 2) + 1

for n in [1024, 1_048_576]:
    print(n, work_a(n), work_b(n), work_c(n), work_d(n))
```

```text
1024 11264 2047 11 2047
1048576 22020096 2097151 21 2097151
```

When `n` grows a thousand times (1024 → 1,048,576):

- **`work_a`** (merge sort) grew about two thousand times: every level is
  `n`, the number of levels is `log n` → `O(n log n)`.
- **`work_b`** grew about a thousand times: the top level is `n`, the one
  below `n/2`, then `n/4`… the total is under `2n`. Most of the work is **at
  the top** → `O(n)`.
- **`work_c`** (binary search) grew by only 10: `O(log n)`.
- **`work_d`** grew a thousand times: each node does 1 work, but there are
  about `2n` nodes. Most of the work is **in the leaves** → `O(n)`.

In short: if the work is the same on every level, `work × log n`; if it
shrinks going down, the top wins; if it grows going down, the leaves win.
Textbooks call this rule the **master theorem**; drawing the tree and adding
up the levels usually gives the same answer.

## The maximum subarray

You have a stock's daily profit/loss: `[2, -5, 6, -2, 3, -8, 4]`. Over which
period of **consecutive days** is the total profit largest? Brute force tries
every start–end pair: `O(n²)`.

With divide and conquer: the best period is either **entirely in the left
half**, **entirely in the right half**, or **crosses the middle**. Recursion
solves the first two. The crossing one is easy: the best sum going left
from the middle + the best sum going right from the middle.

```python
def max_sub(values, lo, hi):
    if lo == hi:                        # a single element
        return values[lo]
    mid = (lo + hi) // 2
    left = max_sub(values, lo, mid)
    right = max_sub(values, mid + 1, hi)
    total, best_left = 0, values[mid]
    for i in range(mid, lo - 1, -1):    # from the middle to the left
        total += values[i]
        best_left = max(best_left, total)
    total, best_right = 0, values[mid + 1]
    for i in range(mid + 1, hi + 1):    # from the middle to the right
        total += values[i]
        best_right = max(best_right, total)
    return max(left, right, best_left + best_right)

values = [2, -5, 6, -2, 3, -8, 4]
print(max_sub(values, 0, len(values) - 1))
```

```text
7
```

The best period is `6, -2, 3`: a total of 7. On each level the crossing parts
take `n` steps in total, with `log n` levels: `O(n log n)`. We counted the
addition steps on 2000 days of random data:

```text
brute force       : 2001000 steps, answer 1115
divide and conquer: 21952 steps, answer 1115
```

The same answer with more than ninety times fewer steps. This problem also
has an `O(n)` solution (Kadane's algorithm); we will see it in the Dynamic
Programming section.

## Multiplying large numbers: Karatsuba

In the multiplication method you learned at school, every digit of one
`n`-digit number is multiplied by every digit of the other: `n²` single-digit
multiplications. Let us split the numbers in two with divide and conquer:

`x = a·10ʰ + b`, `y = c·10ʰ + d` → `x·y = ac·10²ʰ + (ad + bc)·10ʰ + bd`

Four half-size multiplications (`ac`, `ad`, `bc`, `bd`): still `n²`.
**Karatsuba**'s idea from 1960: one multiplication is enough for the middle
term instead of two,

`ad + bc = (a + b)(c + d) − ac − bd`

and `ac` and `bd` were already computed. **Three** multiplications instead of
four:

```python
def karatsuba(x, y):
    if x < 10 or y < 10:                     # a single digit: directly
        return x * y
    half = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10 ** half)
    c, d = divmod(y, 10 ** half)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    middle = karatsuba(a + b, c + d) - ac - bd
    return ac * 10 ** (2 * half) + middle * 10 ** half + bd

print(karatsuba(1234, 5678), 1234 * 5678)
```

```text
7006652 7006652
```

We counted the single-digit multiplications on random numbers (the school
method with the same splitting, using four multiplications):

```text
  8 digits: school     52, karatsuba     39
 64 digits: school   3634, karatsuba   1083
512 digits: school 228676, karatsuba  28375
```

The gap opens as the number of digits grows: in a tree split into three
pieces the number of leaves is `3^(log₂ n) = n^1.58`, with four it is `n²`.
CPython uses this method when multiplying large integers; it is part of why
you can multiply huge numbers like `2 ** 100000` quickly in Python.

## The closest pair of points

There are thousands of points on a plane (shops, sensors, customers); which
**two points are closest** to each other? Brute force looks at every pair:
`n(n−1)/2` distances.

Divide and conquer:

1. Sort the points by `x`, split them in two with a vertical line in the
   middle.
2. Find the closest pair in the two halves with recursion; call the smaller
   one `d`.
3. A pair crossing the line may be closer than `d`, but then both points
   must be closer than `d` to the line. Look only at the points in this
   **strip**; sort the strip by `y`, and each point is compared only with
   neighbours whose `y` difference is below `d`.

<figure class="fig">
<svg viewBox="0 0 420 250" width="420" xmlns="http://www.w3.org/2000/svg">
<rect class="box" x="168" y="8" width="84" height="230" fill-opacity=".35"/>
<line class="curve3" x1="168" y1="8" x2="168" y2="238" stroke-dasharray="5 4"/>
<line class="curve3" x1="252" y1="8" x2="252" y2="238" stroke-dasharray="5 4"/>
<line class="curve" x1="210" y1="4" x2="210" y2="242"/>
<circle class="dot" cx="109.7" cy="40.6" r="5"/>
<circle class="dot2" cx="170.5" cy="51.0" r="5"/>
<circle class="dot" cx="45.3" cy="100.3" r="5"/>
<circle class="dot" cx="368.8" cy="180.1" r="5"/>
<circle class="dot" cx="310.8" cy="64.4" r="5"/>
<circle class="dot2" cx="223.9" cy="75.3" r="5"/>
<circle class="dot" cx="85.6" cy="41.2" r="5"/>
<circle class="dot" cx="101.5" cy="205.5" r="5"/>
<circle class="dot" cx="335.0" cy="181.3" r="5"/>
<circle class="dot" cx="324.2" cy="58.7" r="5"/>
<circle class="dot" cx="137.7" cy="145.4" r="5"/>
<circle class="dot" cx="298.1" cy="190.9" r="5"/>
<circle class="dot" cx="354.4" cy="37.3" r="5"/>
<circle class="dot2" cx="250.2" cy="154.3" r="5"/>
<circle class="dot2" cx="212.3" cy="55.6" r="5"/>
<circle class="dot2" cx="200.0" cy="37.9" r="5"/>
<circle class="dot" cx="375.1" cy="193.1" r="5"/>
<circle class="dot2" cx="228.1" cy="80.0" r="5"/>
<circle class="dot" cx="365.4" cy="134.5" r="5"/>
<circle class="dot" cx="355.3" cy="189.6" r="5"/>
<circle class="dot2" cx="213.2" cy="102.8" r="5"/>
<circle class="dot2" cx="247.6" cy="106.2" r="5"/>
<text class="dim" x="172" y="236" font-size="12">d</text>
<text class="dim" x="240" y="236" font-size="12">d</text>
</svg>
<figcaption>The purple line splits the points in two. A close pair crossing it can only lie in the strip between the dashed lines: only the orange points are compared.</figcaption>
</figure>

```python
import math

def closest(points):                     # points sorted by x
    n = len(points)
    if n <= 3:
        return min((math.dist(p, q) for i, p in enumerate(points)
                    for q in points[i + 1:]), default=math.inf)
    mid = n // 2
    mid_x = points[mid][0]
    d = min(closest(points[:mid]), closest(points[mid:]))
    strip = sorted((p for p in points if abs(p[0] - mid_x) < d),
                   key=lambda p: p[1])
    for i, p in enumerate(strip):
        for q in strip[i + 1:]:
            if q[1] - p[1] >= d:         # the ones above are even farther
                break
            d = min(d, math.dist(p, q))
    return d
```

The number of distances computed by the two methods on 2000 random points:

```text
brute force       : 1999000 distances, closest 0.1504
divide and conquer: 2271 distances, closest 0.1504
```

The same answer with about a thousandth of brute force's distance
computations. It can be proved that each point in the strip looks at only a
few neighbours; the total is `O(n log n)`. The k-d tree from ALG 1 works on
the same idea: split the space in two, rule out the far half.

## When does it not help?

- **When the pieces overlap.** `fib(n) = fib(n−1) + fib(n−2)` splits into two
  pieces, but they solve the same subproblems over and over; it grows
  exponentially. The cure is not divide and conquer but **dynamic
  programming**: solve each subproblem once and keep it.
- **When combining is expensive.** If combining takes `O(n²)`, the gain from
  splitting is lost.
- **When the problem does not shrink.** The pieces must really be smaller;
  with quick sort's bad pivot one piece always stayed `n − 1`.

## Summary

- Divide and conquer: split, solve the pieces with yourself, combine.
- The cost comes from the recursion tree: add up the work on the levels. If
  every level is the same, `work × log n`; if it shrinks going down, the top
  (`O(n)`); if it grows going down, the leaves.
- The maximum subarray: left, right, crossing; `O(n log n)`.
- Karatsuba: three multiplications instead of four; `n^1.58` instead of `n²`.
- The closest pair of points: split, `d`, check only the strip;
  `O(n log n)`.
- If the pieces overlap, dynamic programming.
