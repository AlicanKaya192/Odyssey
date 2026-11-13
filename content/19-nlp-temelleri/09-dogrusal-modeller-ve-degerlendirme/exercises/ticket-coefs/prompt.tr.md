`top_words(label, k)` talep sınıflandırıcısının o sınıf için **en büyük
katsayılı** `k` kelimesini büyükten küçüğe döndürsün. Model ve `words` hazır;
sınıfın satırı `model.coef_` içinde, `model.classes_` sırasıyla.

Eşit puanlı kelimeler abece sırasıyla gelsin: `np.argsort(-puan,
kind="stable")` büyükten küçüğe sıralar ve eşitleri yerinde bırakır,
böylece sıra her bilgisayarda aynı olur.

**Beklenen çıktı:**

```
account account, email, com
billing charged, invoice, billing
refund refund, will, back
shipping delivered, it, arrived
technical app, error, page
```
