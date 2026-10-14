`first_step(message)` modeli çağırmadan önceki kararı versin: mesaj
hazır `DETECT` kalıbına uyuyorsa `["blocked", None]`; yoksa `["model",
sipariş numarası]` (hazır `ORDER_ID`'nin ilk eşleşmesi, yoksa `None`).

**Beklenen çıktı:**

```
['model', 'ORD-48213']
['blocked', None]
['model', None]
```
