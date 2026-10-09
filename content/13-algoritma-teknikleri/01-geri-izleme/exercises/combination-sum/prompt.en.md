Write the function `combination_sum(candidates, target)` **with pruned
backtracking**: from distinct positive integers, each used **at most once**,
it returns every selection whose sum is `target`. Each selection ascending,
the selections in the order they are generated (sort the numbers first).

- `[10, 1, 2, 7, 6, 5]`, `8` → `[[1, 2, 5], [1, 7], [2, 6]]`

`break` as soon as the total passes the target: the next numbers are larger.
The last line counts the selections from 1–40 that make 30; a solution that
walks all `2⁴⁰` subsets without pruning never finishes.

**Expected output:**

```
[[1, 2, 5], [1, 7], [2, 6]]
296
```
