Write the function `lcs_length(a, b)`: it returns the **length** of the
longest common subsequence of two texts (in the same order, not necessarily
next to each other).

On a match `dp[i − 1][j − 1] + 1`, otherwise `max(dp[i − 1][j], dp[i][j − 1])`.

The last line has two texts of 1500 letters; trying every subsequence is
impossible, the table is 2.25 million cells.

**Expected output:**

```
4
5
750
```
