`cheapest(n, roads, start, goal)` fonksiyonunu **Dijkstra** ile yaz: şehirler
`0`..`n − 1`, `roads` `[a, b, maliyet]` **yönlü** yollar (maliyetler negatif
değil). `start`'tan `goal`'a en düşük maliyeti, ulaşılamıyorsa `-1`
döndürsün.

Heap'te `(maliyet, şehir)`; heap'ten eski bir kayıt çıkarsa atla.

**Beklenen çıktı:**

```
4
-1
```
