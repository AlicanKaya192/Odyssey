`shortest_distances(graph, start)` fonksiyonunu **Dijkstra** ile yaz: `graph`
`{düğüm: {komşu: ağırlık}}`; `start`'tan ulaşılabilen her düğümün en kısa
uzaklığını ada göre sıralı bir sözlük olarak döndürsün.

Heap'e `(uzaklık, düğüm)` koy; çıkan düğüm daha önce kesinleştiyse atla;
komşuda `d + w` daha kısaysa güncelle ve heap'e ekle.

**Beklenen çıktı:**

```
A [0, 3, 2, 8, 10, 13]
F [13, 10, 11, 5, 3, 0]
```
