`oov_shares(n_train)` dağarcığı **yalnızca ilk `n_train` yorumla** kursun.
Sonra iki metin grubunda dağarcıkta olmayan token'ların payını (3 basamak)
`[yorumlar, talepler]` olarak döndürsün: yorumlar `REVIEWS[1000:]`,
talepler `TICKETS`. Token'lar vektörleştiricinin `build_analyzer()`'ıyla.

Başlangıç kodu bütün yorumlarla `fit` ediyor; test yorumlarını da görmüş
oluyor.

**Beklenen çıktı:**

```
50 [0.078, 0.637]
200 [0.012, 0.636]
1000 [0.005, 0.635]
```
