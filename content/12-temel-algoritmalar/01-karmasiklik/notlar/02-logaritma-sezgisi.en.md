The logarithm turns up very often in algorithms, and most of the time it is
the answer to a single question: **"How many times can I halve a number
before it gets down to 1?"**

| `n` | Halvings | `log₂ n` (approx.) |
|---|---|---|
| 8 | 8 → 4 → 2 → 1: 3 times | 3 |
| 1 024 | 10 times | 10 |
| 1 000 000 | 19–20 times | 19.9 |
| 1 000 000 000 | 29–30 times | 29.9 |

Another view: `log₂ n` is roughly how many digits `n` has in binary.
1 024 written in binary has 11 digits (`10000000000`).

## Where does it come from in algorithms?

- Algorithms that **discard half of the search at every step**: binary
  search. At most 20 comparisons among a million records.
- **Trees:** a balanced binary tree has height `log₂ n`. In a balanced tree
  of a million elements, 20 steps from the root to a leaf.
- **Divide and conquer:** algorithms that split the list in two and solve
  each half separately (merge sort) go `log₂ n` levels deep; with `n` work
  per level that gives `O(n log n)`.

## The base does not matter

`log₂ n`, `log₁₀ n` and `ln n` are constant multiples of each other
(`log₂ n ≈ 3.32 × log₁₀ n`). Since Big O drops constants we do not write the
base: we just say `O(log n)`.

## To get a feel for it

Looking up a name in a (sorted) phone book, you open it in the middle and
check "further on or further back?". In a 1 000-page book at most 10 openings
are enough. If the book had 1 000 000 pages, 20. The page count grew a
thousandfold; the work only doubled.

The mathematics of the logarithm is in MAT 1's **Logarithms** section.
