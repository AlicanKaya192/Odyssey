Write the function `edit_distance(a, b)`: it returns the fewest **insertions,
deletions, substitutions** needed to turn `a` into `b`. Then
`suggest(word, vocabulary)` returns the closest word in the vocabulary (on a
tie, the one earlier in the list; `min(..., key=...)` already does that).

`dp[i][0] = i`, `dp[0][j] = j`; each cell is the smallest of from above + 1,
from the left + 1, from the diagonal + (1 if the letters differ).

**Expected output:**

```
3
pyhton -> python
nmupy -> numpy
matplotib -> matplotlib
```
