Write the function `ways_to_climb(n)`: it returns in how many different ways a
staircase of `n` steps can be climbed, going up **1 or 2** steps at a time. 1
for `n = 0` (taking no step).

The last step is reached either from one below or from two below:
`ways[i] = ways[i − 1] + ways[i − 2]`.

The last line is `n = 90`; plain recursion never finishes, a table or `@cache`
is needed.

**Expected output:**

```
1 1
2 2
3 3
4 5
5 8
90 4660046610375530309
```
