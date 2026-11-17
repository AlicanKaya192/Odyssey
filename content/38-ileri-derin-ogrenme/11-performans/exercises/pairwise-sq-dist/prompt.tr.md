`pairwise_sq_dist(a, b)` iki nokta listesi arasındaki bütün **kare
uzaklıkları** `(len(a), len(b))` tablosu olarak versin. Başlangıçtaki iç içe
döngü doğru ama yavaş: onu **döngüsüz**, yayınlamayla yaz
(`a[:, None, :] - b[None, :, :]`). Sonucu tam sayı listesi olarak döndür
(`.long().tolist()`).

**Beklenen çıktı:**

```
[[1, 13], [4, 4]]
```
