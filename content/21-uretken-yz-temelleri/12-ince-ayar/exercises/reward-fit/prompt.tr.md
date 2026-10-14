`fit_reward(diffs, steps, lr)` her satırı "tercih edilen − tercih edilmeyen"
özellik farkı olan listeden ödül ağırlıklarını öğrensin: `w` sıfırdan
başlasın; her adımda `p = 1 / (1 + exp(-D @ w))`,
`w += lr * D.T @ (1 - p) / len(D)`. Ağırlıkları 2 basamağa yuvarlanmış
`float` listesi olarak döndür.

**Beklenen çıktı:**

```
[9.3, 4.44]
```
