`kth_highest(scores, k)` fonksiyonunu yaz: 0–100 arası notlardan oluşan
listede **k'inci en yüksek** notu döndürsün (tekrarlar ayrı sayılır).

- `kth_highest([70, 95, 80, 95, 60], 1)` → `95`
- `kth_highest([70, 95, 80, 95, 60], 3)` → `80` (95, 95, 80)

Bütün listeyi sıralama: 101 sayaç kur, sayaçları **100'den aşağı** gez ve
geçtiğin not sayısı `k`'ye ulaşınca o notu döndür. `k` liste boyundan
büyükse `None`.

`sorted` ve `.sort()` kullanma.

**Beklenen çıktı:**

```
95
80
None
```
