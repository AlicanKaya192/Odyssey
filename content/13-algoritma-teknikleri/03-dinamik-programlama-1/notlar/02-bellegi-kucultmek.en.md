If each cell of a DP table looks only at the **last few** cells, there is no
need to keep the whole table.

## Fibonacci: two variables

`table[i]` looks only at `table[i − 1]` and `table[i − 2]`. Two variables are
enough instead of a table: memory goes from `O(n)` down to `O(1)` (the
`fib_table` of the previous note was already like this).

## The grid: a single row

`paths[r][c]` looks only at the cell above (`paths[r − 1][c]`) and the cell
on its left (`paths[r][c − 1]`). If we keep a single row and update it from
left to right, before the update a cell holds the value of **the row above**,
while the cell on its left already holds **this row's** new value:

```python
def grid_paths_row(rows, cols, blocked):
    row = [0] * cols
    row[0] = 1
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                row[c] = 0
            elif c > 0:
                row[c] += row[c - 1]          # from above (old) + from the left (new)
    return row[-1]

print(grid_paths_row(3, 3, set()), grid_paths_row(3, 3, {(1, 1)}),
      grid_paths_row(10, 10, set()))
```

```text
6 2 48620
```

The same answers as the two-dimensional table in the lesson; memory is `cols`
instead of `rows × cols`. On large grids or long sequences (edit distance in
DP 2) this can be the difference between fitting in memory and not.

**The price:** you only find the answer. To recover **how** the answer was
formed (which coins, which path) you need the whole table.
