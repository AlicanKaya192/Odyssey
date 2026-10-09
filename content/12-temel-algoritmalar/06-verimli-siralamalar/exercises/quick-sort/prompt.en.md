Write the function `quick_sort(items)` **recursively**: it returns a sorted
copy of the list.

1. A list of 0 or 1 elements is already sorted.
2. Choose the pivot **at random**: `random.choice(items)`.
3. Split the list in three: smaller than the pivot, **equal to the pivot**,
   larger.
4. Sort the smaller and larger ones with `quick_sort`; combine the result as
   `smaller + equal + larger`.

Keeping equal ones apart stops the two sides from becoming unbalanced on
lists with many copies of the same value.

**Speed requirement:** at the end of the code an already sorted list of
20 000 elements is sorted. Taking the last element as pivot would hit the
depth limit; with a random pivot there is no problem.

**Expected output:**

```
[1, 2, 3, 6, 6, 6, 9]
[]
True
```
