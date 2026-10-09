`first_repeat(items)` fonksiyonunu yaz: listeyi baştan okurken **ikinci kez
görülen ilk** değeri döndürsün; tekrar yoksa `None`.

- `[3, 1, 4, 1, 5, 3]` → `1` (3 daha önce başladı ama 1'in ikincisi önce geldi)

Son satırdaki büyük girdi `O(n²)` bir çözümü süre sınırına takar; `O(n)` gerekir. `count` ve `index` yok.

**Beklenen çıktı:**

```
1
None
199999
```
