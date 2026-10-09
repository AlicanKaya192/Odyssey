`apply_updates(n, updates)` fonksiyonunu **fark dizisiyle** yaz: `n`
günlük, başta hepsi 0 olan bir sayaç listesi düşün. `updates` `[lo, hi,
miktar]` üçlülerinin listesi; her biri `lo`'dan `hi`'ye (**ikisi de dahil**)
her güne `miktar` ekliyor. Bütün güncellemelerden sonraki listeyi döndür.

Her güncellemeyi aralığın her gününe tek tek uygulama: `diff[lo] += miktar`,
`diff[hi + 1] -= miktar`, sonunda bir önek toplamı.

**Beklenen çıktı:**

```
[5, 8, 8, 2, 2, -1]
[0, 0, 0]
```
