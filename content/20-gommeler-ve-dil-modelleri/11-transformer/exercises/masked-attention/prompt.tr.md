`masked_attention(X)` sorgu, anahtar ve değeri `X`'in kendisi alan kendi
kendine dikkatin ağırlık tablosunu döndürsün: puanlar `X @ X.T / √d`,
köşegen üstü `-inf`, her satıra softmax, 3 basamak.

**Beklenen çıktı:**

```
[1.0, 0.0, 0.0]
[0.33, 0.67, 0.0]
[0.248, 0.248, 0.503]
```
