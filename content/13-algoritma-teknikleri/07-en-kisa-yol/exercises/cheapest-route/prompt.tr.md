`cheapest_route(graph, start, goal)` fonksiyonunu yaz: en kısa yolun
uzunluğunu ve yolun kendisini `[uzunluk, [düğümler]]` olarak döndürsün; yol
yoksa `None`.

Dijkstra'da güncellediğin her düğümün `parent`'ını yaz; sonra hedeften
geriye yürüyüp listeyi ters çevir.

**Beklenen çıktı:**

```
[13, ['A', 'C', 'B', 'D', 'E', 'F']]
[10, ['F', 'E', 'D', 'B']]
```
