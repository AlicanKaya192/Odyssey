Write the function `count_subsets(items, limit)` with **meet in the middle**:
it returns the number of subsets (the empty set included) whose total does not
exceed `limit`.

Split the items in two, compute all subset sums of each half, sort one, and
for each sum of the other count the partners with `bisect_right`. On the 30
items on the last line, trying the `2³⁰` subsets one by one runs out of
time.

**Expected output:**

```
6
46879146
```
