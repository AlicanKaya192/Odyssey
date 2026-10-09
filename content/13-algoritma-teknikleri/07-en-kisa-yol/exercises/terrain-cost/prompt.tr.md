`min_cost(grid)` fonksiyonunu yaz: `grid[r][c]` o hücreye girmenin maliyeti.
Sol üstten (başlangıcın maliyeti de sayılır) sağ alta dört yönde giderek en
düşük toplam maliyeti döndürsün.

Hücreler düğüm, maliyetler ağırlık: Dijkstra. BFS yanlış (ağırlıklı),
yalnızca sağa/aşağı giden DP de yanlış (bazen geri dönmek ucuz). Son satırda
150 × 150'lik bir arazi var.

**Beklenen çıktı:**

```
7
7
1488
```
