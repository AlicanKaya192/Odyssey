`store_share(stores, sales)` her satışın **kendi mağazasının** toplam
satışındaki payını 3 basamağa yuvarlı liste olarak döndürsün. Grup toplamını
satırlara `groupby(...).transform("sum")` ile yay; `merge` ve döngü gerekmez.
**Döngü yazma.**

**Beklenen çıktı:**

```
[0.1, 1.0, 0.3, 0.6]
```
