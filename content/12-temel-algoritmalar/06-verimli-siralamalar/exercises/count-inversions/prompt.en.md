The inversion count (the number of pairs with `i < j` but `items[i] >
items[j]`) is `O(n²)` with nested loops. With merge sort it can be counted in
`O(n log n)`: when, during the merge, an element from the right is taken
before the ones on the left, **all the remaining elements on the left** are
bigger than it; each of them is one inversion.

Write the function `sort_and_count(items)`: it returns the tuple
`(sorted_list, inversions)`.

- Base case: 0 or 1 elements → `(items, 0)`.
- Take the results of the two halves: `(left, a)` and `(right, b)`.
- While merging, if `right[j] < left[i]`, `count += len(left) - i`.
- Result: `(merged, a + b + count)`.

**Speed requirement:** at the end of the code a shuffled list of 50 000
elements is counted; nested loops would not make it in time.

**Expected output:**

```
([1, 2, 3, 4, 5], 3)
([1, 2, 3, 4, 5], 10)
622355072
```
