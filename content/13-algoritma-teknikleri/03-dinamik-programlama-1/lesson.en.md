# Dynamic Programming 1

The Divide and Conquer section ended with a warning: if the pieces
**overlap**, that is the same subproblem comes up again and again, divide and
conquer grows exponentially. **Dynamic programming (DP)** is the cure: solve
each subproblem **once**, keep its answer, and when it is needed again, read
it instead of computing it.

It looks for two conditions:

- **Overlapping subproblems:** the same small problem is needed many times.
- **Optimal substructure:** the answer of the big problem can be built from
  the answers of the small ones.

## The problem: doing the same work again and again

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30), calls)
```

```text
832040 2692537
```

<figure class="fig">
<svg viewBox="0 0 696 274" width="696" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="72.4" y1="192.0" x2="28.4" y2="248.0"/>
<line class="line" x1="72.4" y1="192.0" x2="116.4" y2="248.0"/>
<line class="line" x1="160.4" y1="136.0" x2="72.4" y2="192.0"/>
<line class="line" x1="160.4" y1="136.0" x2="204.4" y2="192.0"/>
<line class="line" x1="336.4" y1="136.0" x2="292.4" y2="192.0"/>
<line class="line" x1="336.4" y1="136.0" x2="380.4" y2="192.0"/>
<line class="line" x1="248.4" y1="80.0" x2="160.4" y2="136.0"/>
<line class="line" x1="248.4" y1="80.0" x2="336.4" y2="136.0"/>
<line class="line" x1="512.4" y1="136.0" x2="468.4" y2="192.0"/>
<line class="line" x1="512.4" y1="136.0" x2="556.4" y2="192.0"/>
<line class="line" x1="600.4" y1="80.0" x2="512.4" y2="136.0"/>
<line class="line" x1="600.4" y1="80.0" x2="644.4" y2="136.0"/>
<line class="line" x1="424.4" y1="24.0" x2="248.4" y2="80.0"/>
<line class="line" x1="424.4" y1="24.0" x2="600.4" y2="80.0"/>
<rect class="box" x="6.0" y="232.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="28.4" y="252.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="50.0" y="176.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="50.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="72.4" y="196.2" font-size="12" text-anchor="middle">f(2)</text>
<rect class="box" x="94.0" y="232.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="116.4" y="252.2" font-size="12" text-anchor="middle">f(0)</text>
<rect class="box" x="138.0" y="120.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="138.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="160.4" y="140.2" font-size="12" text-anchor="middle">f(3)</text>
<rect class="box" x="182.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="204.4" y="196.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="226.0" y="64.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="248.4" y="84.2" font-size="12" text-anchor="middle">f(4)</text>
<rect class="box" x="270.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="292.4" y="196.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="314.0" y="120.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="314.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="336.4" y="140.2" font-size="12" text-anchor="middle">f(2)</text>
<rect class="box" x="358.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="380.4" y="196.2" font-size="12" text-anchor="middle">f(0)</text>
<rect class="box" x="402.0" y="8.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="424.4" y="28.2" font-size="12" text-anchor="middle">f(5)</text>
<rect class="box" x="446.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="468.4" y="196.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="490.0" y="120.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="490.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="512.4" y="140.2" font-size="12" text-anchor="middle">f(2)</text>
<rect class="box" x="534.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="556.4" y="196.2" font-size="12" text-anchor="middle">f(0)</text>
<rect class="box" x="578.0" y="64.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="578.0" y="64.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="600.4" y="84.2" font-size="12" text-anchor="middle">f(3)</text>
<rect class="box" x="622.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="644.4" y="140.2" font-size="12" text-anchor="middle">f(1)</text>
</svg>
<figcaption>The call tree of fib(5). The ones with orange rings are subproblems computed more than once: f(3) twice, f(2) three times.</figcaption>
</figure>

More than two and a half million calls for the 30th Fibonacci number. In the
figure even `fib(5)` computes `fib(3)` twice and `fib(2)` three times; as `n`
grows the repeats grow exponentially. Yet there are only `n + 1` different
subproblems: `fib(0)` to `fib(n)`.

## Memoization

The same function, only with a dictionary: look in the dictionary before
computing the answer, and write to it after computing.

```python
memo = {}
memo_calls = 0

def fib_memo(n):
    global memo_calls
    memo_calls += 1
    if n < 2:
        return n
    if n in memo:                          # solved before: read it
        return memo[n]
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]

print(fib_memo(30), memo_calls)
```

```text
832040 59
```

2,692,537 calls went down to 59. Python gives this ready-made: write
`@functools.cache` above the function, and a call with the same argument
returns from the cache.

```python
from functools import cache

@cache
def fib_cached(n):
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(100))
print(fib_cached.cache_info())
```

```text
354224848179261915075
CacheInfo(hits=98, misses=101, maxsize=None, currsize=101)
```

## Tabulation

Memoization goes top-down. You can do the same work **bottom-up**, without
recursion: start from the small answers and fill a table in order.

```python
def fib_table(n):
    table = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]   # the earlier ones are ready
    return table[n]

print(fib_table(30), fib_table(100))
```

```text
832040 354224848179261915075
```

`n` steps, no recursion depth problem. Since only the last two values are
needed here, even two variables are enough instead of a table (`O(1)` memory).

## The dynamic programming recipe

Five questions when writing a DP solution:

1. **State:** what does `best[a]` mean? (e.g. "the fewest coins for amount
   `a`")
2. **Transition:** how is `best[a]` computed from smaller states?
3. **Base:** what is the answer of the smallest states? (`best[0] = 0`)
4. **Order:** in which order must the table be filled so that the needed
   cells are ready?
5. **Answer:** which cell of the table? (`best[amount]`)

## The fewest coins

The greedy method failed for 6 with coins `[1, 3, 4]`. With DP: if the last
coin given is `c`, the fewest coins for amount `a` is `best[a − c] + 1`; try
every coin and take the smallest.

```python
def min_coins(amount, coins):
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return best

print(min_coins(10, [1, 3, 4]))
```

```text
[0, 1, 2, 1, 1, 2, 2, 2, 2, 3, 3]
```

The table holds the answer for every amount from 0 to 10. `best[6] = 2`
(`3 + 3`); greedy said three. The cost is `O(amount × number of coins)`.

## How many different ways?

The same kind of table also answers **"in how many different ways"** instead
of "at least how many": in how many different ways can you give 10 with 1, 2
and 5?

```python
def count_ways(amount, coins):
    ways = [1] + [0] * amount              # the only way to give 0: no coins
    for c in coins:                        # the coins are the outer loop
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]

print(count_ways(10, [1, 2, 5]), count_ways(100, [1, 5, 10, 25, 50]))
```

```text
10 292
```

The order of the loops matters: since the coins are outside, `2 + 5` and
`5 + 2` count as the same selection (a combination). If the amounts were
outside, the orderings would be counted separately.

## The best period: Kadane

The maximum subarray from the Divide and Conquer section is solved in a single
pass with DP. State: `current` = the sum of the best period **ending here**.
Transition: either add this day to the previous period or start again today.

```python
def kadane(values):
    best = current = values[0]
    for x in values[1:]:
        current = max(x, current + x)      # continue or start again
        best = max(best, current)
    return best

print(kadane([2, -5, 6, -2, 3, -8, 4]))
```

```text
7
```

On the 2000-day data from the Divide and Conquer section the answer is the same: 1115.
This time in only 2000 steps, `O(n)`.

## Paths on a grid

How many paths are there from the top-left corner of a grid to the
bottom-right corner, moving only right and down? A cell is reached either
from above or from the left: `paths[r][c] = paths[r − 1][c] + paths[r][c − 1]`.
A blocked cell gets 0.

```python
def grid_paths(rows, cols, blocked):
    paths = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                up = paths[r - 1][c] if r else 0
                left = paths[r][c - 1] if c else 0
                paths[r][c] = up + left
    return paths[-1][-1]

print(grid_paths(3, 3, set()), grid_paths(3, 3, {(1, 1)}), grid_paths(10, 10, set()))
```

```text
6 2 48620
```

Walking every path one by one means tens of thousands of paths on a 10 × 10
grid; the table fills only 100 cells.

## Summary

- DP: solve overlapping subproblems once and keep them.
- Memoization (top-down, `@cache`) or tabulation (bottom-up).
- The recipe: state, transition, base, order, answer.
- The fewest coins, how many different ways, Kadane (`O(n)`), paths on a
  grid.
- Where greedy fails, DP gives the exact answer; the price is time and memory
  as large as the table.
