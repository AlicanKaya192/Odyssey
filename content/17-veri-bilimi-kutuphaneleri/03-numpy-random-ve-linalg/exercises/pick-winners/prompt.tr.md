`pick(ids, k, seed)` kimlik listesinden **tekrarsız** `k` kişi seçsin
(`default_rng(seed).choice(..., size=k, replace=False)`) ve liste döndürsün.
Başlangıç kodu aynı kişiyi iki kez seçebiliyor.

**Beklenen çıktı:**

```
[102, 104, 105, 107]
```
