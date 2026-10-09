## Hangi algoritma?

| Durum | Algoritma | Maliyet |
|---|---|---|
| Ağırlıksız (her kenar 1) | BFS | `O(n + m)` |
| Ağırlıklı, negatif yok, tek başlangıç | Dijkstra (heap) | `O((n + m) log n)` |
| Negatif kenar olabilir | Bellman–Ford | `O(n · m)` |
| Bütün çiftler, küçük graf | Floyd–Warshall | `O(n³)` |
| Tek hedef, iyi bir tahmin var | A* | çoğu zaman Dijkstra'dan az düğüm |
| Yönlü döngüsüz graf (DAG) | topolojik sırayla gevşet | `O(n + m)` (sonraki bölüm) |

## Gevşetme (relaxation)

Hepsinin ortak adımı:

```python
if dist[a] + w < dist[b]:
    dist[b] = dist[a] + w
    parent[b] = a
```

"`a` üzerinden `b`'ye gitmek şimdiye kadar bilinenden kısa mı?" Algoritmalar
yalnızca bu adımı **hangi sırayla** yaptıklarında ayrılır.

## Sık hatalar

- Negatif kenarlı grafta Dijkstra: sessizce yanlış sonuç.
- Heap'e `(uzaklık, düğüm)` yerine `(düğüm, uzaklık)` koymak: heap ada göre
  sıralar.
- Heap'ten çıkan eski kayıtları atlamamak (`done` ya da `d > dist[node]`
  denetimi): doğru çalışır ama gereksiz iş yapar.
- Ulaşılamayan düğüm: `dist.get(node, math.inf)`; sonuçta sonsuz kalır.
- A*'da tahmini abartmak: daha hızlı ama en kısa yol garantisi kalkar.
