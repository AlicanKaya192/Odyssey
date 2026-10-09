`bellman_ford(n, edges, start)` fonksiyonunu yaz: düğümler `0`..`n − 1`,
kenarlar `[a, b, ağırlık]` (yönlü, ağırlık negatif olabilir). Her düğümün
`start`'tan uzaklığını liste olarak döndürsün; ulaşılamayan için `None`.
Negatif döngü varsa (fazladan bir turda hâlâ güncelleme oluyorsa) `None`
döndürsün.

`n − 1` tur boyunca her kenarı gevşet.

**Beklenen çıktı:**

```
[0, 0, 4, 3]
None
```
