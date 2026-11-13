`top_terms(index, k)` `index` numaralı talebin TF-IDF satırında en ağır `k`
kelimeyi büyükten küçüğe bir liste olarak döndürsün. Vektörleştirici
(`min_df=2`), `X` ve `words` hazır.

Eşit puanlı kelimeler abece sırasıyla gelsin: `np.argsort(-puan,
kind="stable")` büyükten küçüğe sıralar ve eşitleri yerinde bırakır,
böylece sıra her bilgisayarda aynı olur.

**Beklenen çıktı:**

```
0 ['prague', 'slow', 'very']
1 ['acconut', 'friday', 'reset']
2 ['tracking', 'work', 'with']
```
