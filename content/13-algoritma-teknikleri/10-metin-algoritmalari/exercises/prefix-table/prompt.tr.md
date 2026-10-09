`prefix_table(pattern)` fonksiyonunu yaz: KMP'nin önek tablosunu döndürsün.
`table[i]`, `pattern[:i + 1]`'in hem öneki hem soneki olan en uzun parçasının
boyu (parçanın kendisi hariç).

`k` şu ana kadarki eşleşme boyu: uyuşmazlıkta `k = table[k - 1]` ile geri
çekil, eşleşmede `k`'yı artır.

**Beklenen çıktı:**

```
[0, 0, 1, 0, 1, 2]
[0, 1, 0, 1, 2, 2, 3]
[0, 0, 0, 0]
```
