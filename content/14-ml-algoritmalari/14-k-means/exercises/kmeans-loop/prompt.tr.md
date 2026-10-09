`kmeans_loop(X, init, max_iter=100)` fonksiyonunu yaz. Her turda önce
noktaları en yakın merkeze ata, sonra merkezleri ortalamaya taşı; yeni
merkezler eskileriyle aynıysa (`np.allclose`) dur. `(merkezler, tur sayısı)`
döndürsün: merkezler `.round(3).tolist()`, tur sayısı ata adımının kaç kez
yapıldığı.

**Beklenen çıktı:**

```
[[1.25, 1.5], [3.9, 5.1]]
3
```
