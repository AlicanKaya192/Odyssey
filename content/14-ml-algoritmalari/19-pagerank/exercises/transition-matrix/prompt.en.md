Write the function `transition_matrix(links)`: `links[j]` is the list of
pages that page `j` links to; `n = len(links)`. `M[i, j] = 1 / outdegree(j)`
(if `j → i`). A page with no links (an empty list) gets the column `1 / n`.
Return `.round(3).tolist()`.

**Expected output:**

```
[0.0, 0.0, 1.0]
[0.5, 0.0, 0.0]
[0.5, 1.0, 0.0]
```
