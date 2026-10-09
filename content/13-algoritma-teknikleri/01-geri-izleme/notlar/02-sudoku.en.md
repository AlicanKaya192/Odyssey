Sudoku is the best-known example of backtracking: put a number from 1–9 that
follows the rules into an empty square and go on; if no number fits
somewhere, go back and try the next number in the previous square.

```python
def solve(board):
    """board: a list of 9 strings, '.' is an empty square. (solution, nodes)."""
    grid = [list(row) for row in board]
    rows = [set(r) - {"."} for r in grid]
    cols = [{grid[r][c] for r in range(9)} - {"."} for c in range(9)]
    boxes = [{grid[r][c] for r in range(b // 3 * 3, b // 3 * 3 + 3)
              for c in range(b % 3 * 3, b % 3 * 3 + 3)} - {"."} for b in range(9)]
    empty = [(r, c) for r in range(9) for c in range(9) if grid[r][c] == "."]
    nodes = [0]

    def fill(k):
        nodes[0] += 1
        if k == len(empty):
            return True
        r, c = empty[k]
        b = r // 3 * 3 + c // 3
        for digit in "123456789":
            if digit in rows[r] or digit in cols[c] or digit in boxes[b]:
                continue                       # breaks a rule: pruning
            grid[r][c] = digit
            rows[r].add(digit); cols[c].add(digit); boxes[b].add(digit)
            if fill(k + 1):
                return True
            rows[r].remove(digit); cols[c].remove(digit); boxes[b].remove(digit)
        grid[r][c] = "."
        return False

    fill(0)
    return ["".join(row) for row in grid], nodes[0]

puzzle = ["53..7....", "6..195...", ".98....6.",
          "8...6...3", "4..8.3..1", "7...2...6",
          ".6....28.", "...419..5", "....8..79"]
solved, nodes = solve(puzzle)
print(solved[0])
print(solved[8])
print(sum(row.count(".") for row in puzzle), "empty cells,", nodes, "nodes")
```

```text
534678912
345286179
51 empty cells, 4209 nodes
```

Trying 9 numbers in each of the 51 empty squares means `9⁵¹` possibilities;
backtracking that prunes with the rules finishes in a few thousand nodes.
The row, column and box sets make every check `O(1)`.

**Even faster:** fill the empty squares not in order but **starting with the
one that has the fewest options**. A square with a single option is filled at
once, and the tree becomes much narrower. This "most constrained variable
first" rule is the core idea of constraint solvers.
