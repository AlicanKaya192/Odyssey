`replace_first(names, new)` listeyi diziye çevirip ilk elemanı `new` ile
değiştiriyor ve liste döndürüyor; ama dizinin metin genişliği en uzun ilk
ada göre sabitlendiği için `new` kırpılıyor. Diziyi **`dtype=object`** ile
kur ki metin kırpılmasın.

**Beklenen çıktı:**

```
['hello', 'cde']
```
