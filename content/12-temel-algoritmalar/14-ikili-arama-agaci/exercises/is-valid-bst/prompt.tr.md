`is_bst(node, low=None, high=None)` fonksiyonunu yaz: ağaç geçerli bir
ikili arama ağacıysa `True` döndürsün. Her düğüm `low < değer < high`
aralığında olmalı (`None` sınır yok demek); sola inerken üst sınır düğümün
değeri olur, sağa inerken alt sınır. Eşit değer geçersiz. Boş ağaç geçerli.

Yalnızca çocuklara bakmak yetmez:

- `[5, [3, 1, 6], 8]` → `False` (6, 5'in solunda ama 5'ten büyük)
- `[5, [3, 1, 4], 8]` → `True`

Ağaçlar iç içe listeyle yazılıyor: `[deger, sol, sag]`, düz değer yaprak,
`None` boş; `build_tree` hazır.

**Beklenen çıktı:**

```
False
True
True
```
