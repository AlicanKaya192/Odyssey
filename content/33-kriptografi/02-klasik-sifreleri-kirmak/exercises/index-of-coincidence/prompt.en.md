`ioc(text)` should return the index of coincidence of the letters in
the text (case does not matter, non-letters are not counted) with
`round(..., 4)`: sum `n * (n - 1)` over each letter count `n` and divide by
`N * (N - 1)` (`N` is the total number of letters). `0.0` if there are
fewer than two letters.

**Expected output:**

```
0.0682
0.0
1.0
0.0
```
