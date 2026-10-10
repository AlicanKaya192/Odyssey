`time_splits(n, splits, gap)` `n` dönemlik bir seriyi
`TimeSeriesSplit(n_splits=splits, gap=gap)` ile bölsün. Her kat için
`[eğitimin_son_sırası, test_sıraları]` döndürsün (`int(train.max())`,
`test.tolist()`). Başlangıç kodu `KFold` kullanıyor; eğitimde gelecek var.

**Beklenen çıktı:**

```
[3, [4, 5]]
[5, [6, 7]]
[7, [8, 9]]
[9, [10, 11]]
```
