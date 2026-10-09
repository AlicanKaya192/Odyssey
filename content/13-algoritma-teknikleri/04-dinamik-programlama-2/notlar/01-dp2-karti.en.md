## Two-dimensional DPs

| Problem | State | Transition | Cost |
|---|---|---|---|
| 0/1 knapsack | `best[i][w]` | `max(best[i−1][w], best[i−1][w−weight] + value)` | `O(n · W)` |
| Longest common subsequence | `dp[i][j]` | on a match `dp[i−1][j−1] + 1`, otherwise `max(above, left)` | `O(n · m)` |
| Edit distance | `dp[i][j]` | `min(above + 1, left + 1, diagonal + (1 if different))` | `O(n · m)` |
| Longest increasing subsequence | `best[i]` | `max(best[j] + 1)`, `values[j] < values[i]` | `O(n²)`; `O(n log n)` with `bisect` |
| DTW | `dp[i][j]` | `difference + min(above, left, diagonal)` | `O(n · m)` |

## Base rows

- LCS: the first row and column are 0 (nothing in common with an empty text).
- Edit distance: `dp[i][0] = i` (delete all), `dp[0][j] = j` (insert all).
- DTW: `dp[0][0] = 0`, the other edges infinite (no matching while one series
  is empty).
- Knapsack: `best[0][w] = 0` (no items).

## Recovering

The table keeps only **the best value**; for the choices themselves you walk
backwards from the end. In each cell you ask "which option did this value come
from?":

- Knapsack: if it equals the row above, the item was not taken; otherwise it
  was.
- LCS: if the letters are equal, that letter joins the sequence, go to the
  diagonal; otherwise go to the larger neighbour.

Recovering is not possible on a table with shrunk memory (only the last row).

## Common mistakes

- Index shifts: the table is `len + 1` long, the `i`-th letter of the text is
  `a[i − 1]`.
- Taking the same item twice in the knapsack: in the single-row version the
  capacity loop must go **from large to small** (`for w in range(W, weight − 1,
  −1)`); going from small to large takes the item again and again.
- Taking the `tails` list itself as the answer in LIS: `tails` may not be a
  valid subsequence; only its **length** is right.
