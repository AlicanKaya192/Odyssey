Sudoku geri izlemenin en bilinen örneği: boş bir kareye 1–9 arasından kurala
uyan bir sayı koy, devam et; bir yerde hiçbir sayı uymuyorsa geri dön ve bir
önceki karede sıradaki sayıyı dene.

```python
def solve(board):
    """board: 9 metinden oluşan liste, '.' boş kare. (çözüm, düğüm sayısı)."""
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
                continue                       # kural bozuluyor: budama
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

51 boş karenin her birine 9 sayı denemek `9⁵¹` olasılık demek; kurallarla
budayan geri izleme birkaç bin düğümde bitiriyor. Satır, sütun ve kutu
kümeleri her denetimi `O(1)` yapıyor.

**Daha da hızlısı:** boş kareleri sırayla değil, **en az seçeneği olandan**
başlayarak doldurmak. Seçeneği tek olan kare hemen dolar, ağaç çok daha dar
olur. Bu "en kısıtlı değişken önce" kuralı kısıt çözücülerin (constraint
solver) temel fikri.
