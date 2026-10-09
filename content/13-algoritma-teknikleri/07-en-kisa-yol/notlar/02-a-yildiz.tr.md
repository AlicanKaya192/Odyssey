Derste A*'ın sonuçlarını gördük; kodu şu. Dijkstra'dan tek farkı heap'e
konan anahtar: `gelinen yol + hedefe tahmin`. Eşitlikte derinde olanı
(`g` büyük) öne almak için ikinci alan `-g`.

```python
import heapq
import math

def astar(grid):
    rows, cols = len(grid), len(grid[0])
    goal = (rows - 1, cols - 1)

    def estimate(r, c):                     # Manhattan: hedefe en az bu kadar
        return abs(r - goal[0]) + abs(c - goal[1])

    best = {(0, 0): 0}
    heap = [(estimate(0, 0), 0, 0, 0)]      # (f, -g, satır, sütun)
    expanded = 0
    while heap:
        f, neg_g, r, c = heapq.heappop(heap)
        g = -neg_g
        if g > best[(r, c)]:
            continue                        # eski kayıt
        expanded += 1
        if (r, c) == goal:
            return g, expanded
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < rows and 0 <= nc < cols
            free = inside and grid[nr][nc] == "."
            if free and g + 1 < best.get((nr, nc), math.inf):
                best[(nr, nc)] = g + 1
                heapq.heappush(heap, (g + 1 + estimate(nr, nc), -(g + 1), nr, nc))
    return -1, expanded

grid = ["....#...",
        ".##.#.#.",
        ".#....#.",
        ".#.##.#.",
        "...#..#."]
print(astar(grid))
```

```text
(15, 27)
```

`estimate` sabit 0 döndürseydi bu kod Dijkstra'nın aynısı olurdu. Tahmin
**kabul edilebilir** (admissible, gerçek uzaklığı aşmayan) olduğu sürece ilk
çıkan hedef en kısa yoldur. Çapraz hareket serbestse Manhattan abartır;
o zaman Chebyshev ya da Öklid uzaklığı kullanılır.
