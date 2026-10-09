`sq_distances(A, B)` fonksiyonunu yaz: `A`'nın her satırı ile `B`'nin her
satırı arasındaki **kare** Öklid uzaklığını `(len(A), len(B))` matris olarak
döndürsün (`.round(4).tolist()`).

Döngü yok: yayın `A[:, None, :] − B[None, :, :]`.

**Beklenen çıktı:**

```
[[1.0, 25.0, 0.0], [1.0, 13.0, 2.0]]
```
