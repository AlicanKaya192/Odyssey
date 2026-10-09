`level_sums(root)` fonksiyonunu **kuyrukla (BFS)** yaz: her seviyedeki
değerlerin toplamını, kökten başlayarak bir liste olarak döndürsün. Boş ağaç
için `[]`.

- Dersteki ağaç: seviyeler `[1]`, `[2, 3]`, `[4, 5, 6]` → `[1, 5, 15]`

`collections.deque` ve `for _ in range(len(queue))` kalıbını kullan.

Ağaçlar iç içe listeyle yazılıyor: `[deger, sol, sag]`, düz bir değer
yaprak, `None` boş. `build_tree` bunu `TreeNode`'lara çeviriyor; `TREE`
dersteki ağaç (`[1, [2, 4, 5], [3, None, 6]]`).

**Beklenen çıktı:**

```
[1, 5, 15]
[]
```
