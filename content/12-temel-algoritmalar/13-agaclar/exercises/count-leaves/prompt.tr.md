`count_leaves(node)` fonksiyonunu yaz: ağaçtaki **yaprak** sayısını
döndürsün. Yaprak, sol **ve** sağ çocuğu `None` olan düğüm. Boş ağaç için `0`.

Tek çocuklu bir düğüm yaprak değil: `[1, [2, [3, None, 4], None], None]`
zincirinde yalnızca `4` yaprak.

Ağaçlar iç içe listeyle yazılıyor: `[deger, sol, sag]`, düz bir değer
yaprak, `None` boş. `build_tree` bunu `TreeNode`'lara çeviriyor; `TREE`
dersteki ağaç (`[1, [2, 4, 5], [3, None, 6]]`).

**Beklenen çıktı:**

```
3
1
0
```
