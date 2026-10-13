Word2Vec saymıyor gibi görünüyor ama aslında saymaya çok yakın bir şey
yapıyor. Levy ve Goldberg (2014), olumsuz örneklemeli atlamalı gramın
eğitimin sonunda `v_kelime · u_bağlam ≈ PMI(kelime, bağlam) − log K`
eşitliğine doğru gittiğini gösterdi (K olumsuz örnek sayısı). Yani Word2Vec,
**kaydırılmış bir PMI matrisini** dolaylı yoldan iki küçük matrisin çarpımı
olarak yazıyor; önceki bölümde PPMI'ı SVD ile yazdığımız gibi.

Dersteki eğitilmiş `W_in` ve `W_out` ile bakalım. En az 20 kez birlikte
geçen çiftlerde nokta çarpımı `PMI − log 5` ile karşılaştırıyoruz:

```python
X = W_in @ W_out.T
M = np.zeros((len(vocab), len(vocab)))
np.add.at(M, (pairs[:, 0], pairs[:, 1]), 1)
with np.errstate(divide="ignore"):
    pmi = np.log(M * M.sum() / np.outer(M.sum(axis=1), M.sum(axis=0)))
seen = M >= 20
shifted = pmi[seen] - np.log(5)
print(seen.sum(), round(float(np.corrcoef(X[seen], shifted)[0, 1]), 3))
print(round(float(X[seen].mean()), 2), round(float(shifted.mean()), 2))
```

```text
2076 0.865
0.13 0.2
```

- 2076 çiftte korelasyon 0,865: nokta çarpımlar kaydırılmış PMI'ı büyük
  ölçüde izliyor. Ortalamaları da yakın (0,13 ve 0,2).
- Tam eşitlik yok: model yalnızca beş tur eğitildi, vektörler 20 boyutlu ve
  eşitlik ancak çok uzun eğitimde ve yeterince boyutta beklenir.
- Ders: "sayma" ve "tahmin etme" iki ayrı dünya değil. İkisi de bir PMI
  matrisini küçük boyutlara sıkıştırıyor; farklar ağırlıklandırmada,
  eğitim yönteminde ve ayarlarda. Bu yüzden iyi ayarlanmış PPMI + SVD
  birçok testte Word2Vec'e yakın sonuç verir.
