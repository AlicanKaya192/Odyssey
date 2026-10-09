Write the function `hill_climb(x, step)`: `f` is ready. At each step look at
the one of `x - step` and `x + step` with the smaller `f`
(`min(..., key=f)`); if it is not better than `x`, stop and return
`round(x, 2)`, otherwise move there.

**Expected output:**

```
-20 -20
-5 -7.7
0 -1.5
4 4.6
18 16.9
```
