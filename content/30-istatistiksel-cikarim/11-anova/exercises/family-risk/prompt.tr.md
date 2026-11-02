`family_risk(k, alpha)` `k` grup için çift sayısını ve bu çiftler bağımsız
olsaydı en az bir yanlış alarm olasılığını döndürsün: `[çift, risk]`. Çift
sayısı `k * (k - 1) // 2`, risk `1 - (1 - alpha) ** çift` (3 basamak).
Başlangıç kodu çift sayısını grup sayısı, riski de `alpha` sanıyor.

**Beklenen çıktı:**

```text
[6, 0.265]
[45, 0.901]
```
