`count_components(n, edges)` fonksiyonunu yaz: `0`'dan `n − 1`'e kadar
numaralı düğümlerin kaç **bağlı bileşene** ayrıldığını döndürsün. Hiç kenarı
olmayan düğüm de tek başına bir bileşen.

Her ziyaret edilmemiş düğümden yeni bir BFS (ya da yığınlı DFS) başlat.
Son satırdaki 200 000 düğümlük zincirde özyineli DFS derinlik sınırına
takılır.

**Beklenen çıktı:**

```
2
4
1
```
