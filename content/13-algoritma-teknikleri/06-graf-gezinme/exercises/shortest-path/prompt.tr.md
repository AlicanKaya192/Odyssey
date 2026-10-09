`shortest_path(edges, start, goal)` fonksiyonunu yaz: BFS ile en az adımlı
yolu düğüm listesi olarak döndürsün; yol yoksa `None`. Komşulara **alfabetik
sırayla** bak (eşit uzunlukta yollardan hangisinin seçileceği buna bağlı).

Her düğümün ebeveynini `parent` sözlüğünde tut; hedeften geriye yürüyüp
listeyi ters çevir.

**Beklenen çıktı:**

```
['ada', 'bora', 'deniz', 'ece', 'fuat']
['cem', 'deniz', 'ece']
None
```
