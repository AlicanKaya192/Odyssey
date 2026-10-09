`distances(edges, start)` fonksiyonunu **BFS** ile yaz: `start`'tan
ulaşılabilen her düğümün kaç adım uzakta olduğunu veren sözlüğü döndürsün.

Uzaklık sözlüğü aynı zamanda ziyaret edilenler kümesi: sözlükte olmayan
komşuya `uzaklık + 1` yaz ve kuyruğa ekle. `build_graph` hazır.

**Beklenen çıktı:**

```
ada 0
bora 1
cem 1
deniz 2
ece 3
fuat 4
{'gul': 0, 'hakan': 1}
```
