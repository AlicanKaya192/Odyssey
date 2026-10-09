`point_types(X, eps, min_samples)` fonksiyonunu yaz: her nokta için
`"core"`, `"border"` ya da `"noise"`. Çekirdek: `eps` içinde (kendisi dahil)
en az `min_samples` nokta. Sınır: çekirdek değil ama `eps` içinde bir
çekirdek var. Gerisi gürültü. Listeyi döndürsün.

**Beklenen çıktı:**

```
0 core
1 core
2 core
3 core
4 border
5 noise
```
