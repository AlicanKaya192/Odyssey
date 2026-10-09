# Dynamic Programming 2

In DP 1 the tables were one-dimensional or a grid. This section has the four
most used examples of two-dimensional tables: the whole (0/1) knapsack, the
common part of two texts, the edit distance between two texts and the longest
increasing subsequence. At the end, an example from data science: dynamic
time warping (DTW), which compares time series. And a new skill: recovering
from the table not only the answer but **how the answer was formed**.

## The whole (0/1) knapsack

The greedy method found 160 for a 50-kilo bag with items `(60, 10)`,
`(100, 20)`, `(120, 30)`; the right answer is 220. With DP the state is:
`best[i][w]` = the largest value that can be taken **with the first `i`
items** and **`w` kilos** of capacity. For the `i`-th item there are two
options: leave it (`best[i − 1][w]`) or, if it fits, take it
(`best[i − 1][w − weight] + value`).

```python
def knapsack(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]                    # leave it
            if weight <= w and best[i - 1][w - weight] + value > best[i][w]:
                best[i][w] = best[i - 1][w - weight] + value   # take it
    chosen, w = [], capacity                               # recover
    for i in range(n, 0, -1):
        if best[i][w] != best[i - 1][w]:                   # this item was taken
            chosen.append(i - 1)
            w -= items[i - 1][1]
    return best[n][capacity], sorted(chosen)

print(knapsack([(60, 10), (100, 20), (120, 30)], 50))
```

```text
(220, [1, 2])
```

220, the second and third items (indexes 1 and 2). **Recovering** walks
backwards from the last cell of the table: if the value equals the row above,
that item was not taken; if it differs, it was taken and the capacity drops by
its weight. The cost is `O(items × capacity)`.

## The longest common subsequence (LCS)

The longest sequence of letters that appears **in the same order** in two
texts (they do not need to be next to each other). File comparison (`diff`),
aligning DNA sequences and plagiarism checks are built on it. The state:
`dp[i][j]` = the length of the common subsequence of the first `i` letters of
`a` and the first `j` letters of `b`.

<figure class="fig">
<svg viewBox="0 0 258 290" width="258" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="48.0" y="22" font-size="13" text-anchor="middle"></text>
<text class="dim" x="80.0" y="22" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="112.0" y="22" font-size="13" text-anchor="middle">D</text>
<text class="dim" x="144.0" y="22" font-size="13" text-anchor="middle">C</text>
<text class="dim" x="176.0" y="22" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="208.0" y="22" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="240.0" y="22" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="20" y="52.5" font-size="13" text-anchor="middle"></text>
<text class="dim" x="20" y="84.5" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="20" y="116.5" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="20" y="148.6" font-size="13" text-anchor="middle">C</text>
<text class="dim" x="20" y="180.6" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="20" y="212.6" font-size="13" text-anchor="middle">D</text>
<text class="dim" x="20" y="244.6" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="20" y="276.6" font-size="13" text-anchor="middle">B</text>
<rect class="box" x="32" y="32" width="32" height="32"/>
<text class="ink" x="48.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="32" width="32" height="32"/>
<text class="ink" x="80.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="96" y="32" width="32" height="32"/>
<text class="ink" x="112.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="128" y="32" width="32" height="32"/>
<text class="ink" x="144.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="160" y="32" width="32" height="32"/>
<text class="ink" x="176.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="192" y="32" width="32" height="32"/>
<text class="ink" x="208.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="224" y="32" width="32" height="32"/>
<text class="ink" x="240.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="32" y="64" width="32" height="32"/>
<text class="ink" x="48.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="64" width="32" height="32"/>
<text class="ink" x="80.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="96" y="64" width="32" height="32"/>
<text class="ink" x="112.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="128" y="64" width="32" height="32"/>
<text class="ink" x="144.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="160" y="64" width="32" height="32"/>
<text class="ink" x="176.0" y="84.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="192" y="64" width="32" height="32"/>
<text class="ink" x="208.0" y="84.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="224" y="64" width="32" height="32"/>
<text class="ink" x="240.0" y="84.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="32" y="96" width="32" height="32"/>
<text class="ink" x="48.0" y="116.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="96" width="32" height="32"/>
<rect class="curve4" x="66" y="98" width="28" height="28" rx="4"/>
<text class="ink" x="80.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="96" width="32" height="32"/>
<text class="ink" x="112.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="128" y="96" width="32" height="32"/>
<text class="ink" x="144.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="160" y="96" width="32" height="32"/>
<text class="ink" x="176.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="192" y="96" width="32" height="32"/>
<text class="ink" x="208.0" y="116.5" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="224" y="96" width="32" height="32"/>
<text class="ink" x="240.0" y="116.5" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="32" y="128" width="32" height="32"/>
<text class="ink" x="48.0" y="148.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="128" width="32" height="32"/>
<text class="ink" x="80.0" y="148.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="128" width="32" height="32"/>
<text class="ink" x="112.0" y="148.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="128" y="128" width="32" height="32"/>
<rect class="curve4" x="130" y="130" width="28" height="28" rx="4"/>
<text class="ink" x="144.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="128" width="32" height="32"/>
<text class="ink" x="176.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="192" y="128" width="32" height="32"/>
<text class="ink" x="208.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="224" y="128" width="32" height="32"/>
<text class="ink" x="240.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="32" y="160" width="32" height="32"/>
<text class="ink" x="48.0" y="180.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="160" width="32" height="32"/>
<text class="ink" x="80.0" y="180.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="160" width="32" height="32"/>
<text class="ink" x="112.0" y="180.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="128" y="160" width="32" height="32"/>
<text class="ink" x="144.0" y="180.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="160" width="32" height="32"/>
<text class="ink" x="176.0" y="180.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="192" y="160" width="32" height="32"/>
<rect class="curve4" x="194" y="162" width="28" height="28" rx="4"/>
<text class="ink" x="208.0" y="180.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="224" y="160" width="32" height="32"/>
<text class="ink" x="240.0" y="180.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="32" y="192" width="32" height="32"/>
<text class="ink" x="48.0" y="212.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="192" width="32" height="32"/>
<text class="ink" x="80.0" y="212.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="192" width="32" height="32"/>
<text class="ink" x="112.0" y="212.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="128" y="192" width="32" height="32"/>
<text class="ink" x="144.0" y="212.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="192" width="32" height="32"/>
<text class="ink" x="176.0" y="212.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="192" y="192" width="32" height="32"/>
<text class="ink" x="208.0" y="212.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="224" y="192" width="32" height="32"/>
<text class="ink" x="240.0" y="212.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="32" y="224" width="32" height="32"/>
<text class="ink" x="48.0" y="244.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="224" width="32" height="32"/>
<text class="ink" x="80.0" y="244.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="224" width="32" height="32"/>
<text class="ink" x="112.0" y="244.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="128" y="224" width="32" height="32"/>
<text class="ink" x="144.0" y="244.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="224" width="32" height="32"/>
<text class="ink" x="176.0" y="244.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="192" y="224" width="32" height="32"/>
<text class="ink" x="208.0" y="244.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="224" y="224" width="32" height="32"/>
<rect class="curve4" x="226" y="226" width="28" height="28" rx="4"/>
<text class="ink" x="240.0" y="244.6" font-size="13" text-anchor="middle">4</text>
<rect class="box" x="32" y="256" width="32" height="32"/>
<text class="ink" x="48.0" y="276.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="256" width="32" height="32"/>
<text class="ink" x="80.0" y="276.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="256" width="32" height="32"/>
<text class="ink" x="112.0" y="276.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="128" y="256" width="32" height="32"/>
<text class="ink" x="144.0" y="276.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="256" width="32" height="32"/>
<text class="ink" x="176.0" y="276.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="192" y="256" width="32" height="32"/>
<text class="ink" x="208.0" y="276.6" font-size="13" text-anchor="middle">4</text>
<rect class="box" x="224" y="256" width="32" height="32"/>
<text class="ink" x="240.0" y="276.6" font-size="13" text-anchor="middle">4</text>
</svg>
<figcaption>The table of ABCBDAB (rows) and BDCABA (columns). The green cells are the letters matched while recovering: B, C, B, A.</figcaption>
</figure>

```python
def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1        # a match: +1 from the diagonal
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    out, i, j = [], len(a), len(b)                     # recover
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[-1][-1], "".join(reversed(out))

print(lcs("ABCBDAB", "BDCABA"))
```

```text
(4, 'BCBA')
```

## Edit distance (Levenshtein)

The fewest **insertions, deletions or substitutions** needed to turn one text
into the other. Spell checking, "did you mean?" suggestions and matching
records with spelling differences during data cleaning use it. Each cell is the
cheapest of three options: from above (deletion), from the left (insertion),
from the diagonal (free if the letters match, otherwise a substitution).

```python
def edit_distance(a, b):
    prev = list(range(len(b) + 1))           # from the empty text to b: j insertions
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1,        # deletion
                         cur[j - 1] + 1,     # insertion
                         prev[j - 1] + cost) # substitution or match
        prev = cur
    return prev[-1]

print(edit_distance("kitten", "sitting"), edit_distance("python", "pyhton"))

words = ["pandas", "numpy", "python", "matplotlib", "seaborn", "sklearn"]
for typo in ["pyhton", "pnadas", "numpi", "seborn"]:
    print(typo, "->", min(words, key=lambda w: edit_distance(typo, w)))
```

```text
3 2
pyhton -> python
pnadas -> pandas
numpi -> numpy
seborn -> seaborn
```

Instead of the whole table we keep only the previous row (the "shrinking the
memory" note of DP 1): memory `O(len(b))`. Swapping two letters (`pyhton`)
counts as two operations here.

## The longest increasing subsequence (LIS)

The longest **increasing** subsequence that can be picked from a sequence
without changing the order. The state: `best[i]` = the length of the longest
increasing subsequence **ending** at the `i`-th element; for every `i` all
earlier `j`s are checked: `O(n²)`.

A cleverer way is `O(n log n)`: `tails[k]` is **the smallest last element** of
the increasing subsequences of length `k + 1`. Since this list is always
sorted, each new element is put in its place with `bisect`.

```python
import bisect

def lis_slow(values):
    best = [1] * len(values)
    for i in range(len(values)):
        for j in range(i):
            if values[j] < values[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return max(best, default=0)

def lis_fast(values):
    tails = []
    for x in values:
        k = bisect.bisect_left(tails, x)     # the place of x
        if k == len(tails):
            tails.append(x)                  # a longer subsequence
        else:
            tails[k] = x                     # same length, a smaller end
    return len(tails)

print(lis_slow([10, 9, 2, 5, 3, 7, 101, 18]), lis_fast([10, 9, 2, 5, 3, 7, 101, 18]))
```

```text
4 4
```

The two methods on 5000 random numbers:

```text
O(n^2)       : 135 in 469.7 ms
O(n log n)   : 135 in 0.47 ms
```

## In data science: dynamic time warping (DTW)

When comparing two time series, matching the points **at the same time**
(Euclidean or absolute difference) shows a big difference if the same shape
is a little shifted. **Dynamic time warping** allows a point of one series to
be matched with **nearby** points of the other; it finds the cheapest matching
with the same table as edit distance.

```python
import math

def dtw(a, b):
    dp = [[math.inf] * (len(b) + 1) for _ in range(len(a) + 1)]
    dp[0][0] = 0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = abs(a[i - 1] - b[j - 1])
            dp[i][j] = cost + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[-1][-1]

wave = [0, 1, 3, 4, 3, 1, 0, 0, 0]
late = [0, 0, 0, 1, 3, 4, 3, 1, 0]       # the same wave, two steps late
other = [4, 3, 1, 0, 0, 0, 1, 3, 4]      # a different shape
point = lambda a, b: sum(abs(x - y) for x, y in zip(a, b))
print("same shape, late :", point(wave, late), dtw(wave, late))
print("other shape      :", point(wave, other), dtw(wave, other))
```

```text
same shape, late : 14 0
other shape      : 24 15
```

With the point-by-point difference the same wave arriving late (14) looks
close to a different shape (24); with DTW the same wave is 0 and the different
shape 15. Speech recognition, recognising movement in sensor data and time
series clustering use DTW.

## Summary

- 0/1 knapsack: `best[i][w]`, take it or leave it; `O(items × capacity)`.
- LCS: on a match +1 from the diagonal, otherwise the larger of above and left.
- Edit distance: the cheapest of deletion, insertion and substitution; spell
  checking and record matching.
- LIS: an `O(n²)` DP or `O(n log n)` with `bisect`.
- Recovering: walk backwards from the end of the table by looking at which
  choice was made.
- DTW: a DP that matches shifted time series.
