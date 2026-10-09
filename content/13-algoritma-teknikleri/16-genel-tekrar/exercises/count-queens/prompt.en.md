Write the function `count_queens(n)` with **backtracking**: it returns in how
many different ways `n` queens that do not threaten each other can be placed
on an `n × n` board.

Place row by row; keep the used columns and the two diagonals
(`row − column`, `row + column`) in sets. If they are in the sets, do not try
that square at all (pruning).

**Expected output:**

```
1 1
2 0
3 0
4 2
5 10
6 4
7 40
8 92
```
