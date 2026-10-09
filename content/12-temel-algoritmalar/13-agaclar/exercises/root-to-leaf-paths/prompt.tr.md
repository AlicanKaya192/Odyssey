`paths(root)` fonksiyonunu yaz: kökten her yaprağa giden yolu `"1->2->4"`
biçiminde bir metin olarak, **soldan sağa** sırayla bir liste hâlinde
döndürsün. Boş ağaç için `[]`.

- Dersteki ağaç → `["1->2->4", "1->2->5", "1->3->6"]`

İpucu: yardımcı bir fonksiyon o ana kadarki yolu (`prefix`) taşıyarak aşağı
insin; yaprağa varınca yolu listeye eklesin.

Ağaçlar iç içe listeyle yazılıyor: `[deger, sol, sag]`, düz bir değer
yaprak, `None` boş. `build_tree` bunu `TreeNode`'lara çeviriyor; `TREE`
dersteki ağaç (`[1, [2, 4, 5], [3, None, 6]]`).

**Beklenen çıktı:**

```
1->2->4
1->2->5
1->3->6
[]
```
