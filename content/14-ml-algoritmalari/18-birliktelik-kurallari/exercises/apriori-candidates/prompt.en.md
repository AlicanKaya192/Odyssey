Write the function `candidates(frequent)`: `frequent` is a list of
frequent sets of the same size (`k`). The union of two sets is a candidate if
it has `k + 1` items; but drop it unless **all** its `k`-item subsets are in
`frequent`. Return the candidates as sorted lists, in sorted order
(`sorted`).

**Expected output:**

```
['bread', 'butter', 'milk']
```
