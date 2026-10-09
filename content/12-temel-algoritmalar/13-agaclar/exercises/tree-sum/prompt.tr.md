`tree_sum(node)` fonksiyonunu **özyinelemeyle** yaz: ağaçtaki bütün
değerlerin toplamını döndürsün. Boş ağaç (`None`) için `0`.

Ağaçlar iç içe listeyle yazılıyor: `[deger, sol, sag]`, düz bir değer
yaprak, `None` boş. `build_tree` bunu `TreeNode`'lara çeviriyor; `TREE`
dersteki ağaç (`[1, [2, 4, 5], [3, None, 6]]`).

**Beklenen çıktı:**

```
21
0
```
