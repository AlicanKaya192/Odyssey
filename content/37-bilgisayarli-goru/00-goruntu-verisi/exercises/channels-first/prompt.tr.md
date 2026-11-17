`channels_first(img)` `(yükseklik, genişlik, kanal)` sırasındaki iç içe bir
listeyi `(kanal, yükseklik, genişlik)` sırasına çevirip yine iç içe liste
olarak döndürsün. `torch.tensor`, `permute` ve `tolist` yeter.

**Beklenen çıktı:**

```
3 2 2
[[1, 4], [7, 10]]
```
