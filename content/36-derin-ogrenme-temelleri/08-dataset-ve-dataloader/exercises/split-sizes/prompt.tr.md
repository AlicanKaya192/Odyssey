`split_sizes(n, train_fraction)` `n` örneği `random_split` ile (tohum 0) eğitim ve
test diye ayırsın: eğitime `int(n * train_fraction)` örnek. `[eğitim boyu, test
boyu, ortak örnek sayısı]` döndürsün. Ortak sayısı için iki parçanın `indices`'ini
küme olarak kesiştir.

**Beklenen çıktı:**

```
[80, 20, 0]
[3, 4, 0]
```
