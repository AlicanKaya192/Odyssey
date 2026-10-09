`kfold_folds(n, k)` fonksiyonunu yaz: `0..n−1` indekslerini `k` **ardışık**
kata böl ve her katın test indekslerini liste olarak döndürsün. `n`, `k`'ya
bölünmezse **ilk** `n % k` kat birer fazla örnek alır (scikit-learn'ün
`KFold`'u gibi).

`KFold` yok.

**Beklenen çıktı:**

```
[0, 1, 2, 3]
[4, 5, 6, 7]
[8, 9, 10]
```
