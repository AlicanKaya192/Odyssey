Write the function `count_queens(n)`: it returns in how many different ways
`n` queens that do not attack each other can be placed on an `n × n` board.

Put one queen in each row; keep the used columns and the two diagonal
directions (`row - col`, `row + col`) in three sets, and never try a square
under attack.

The last line, `n = 11` (trying every ordering would be `11!` ≈ 40 million
boards), must finish within the time limit.

**Expected output:**

```
4 2
6 4
8 92
11 2680
```
