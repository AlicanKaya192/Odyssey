`bucket` hazır. `assign(user_id, salt, share_b=50)` kova `share_b`'den
**küçükse** `"B"`, değilse `"A"` döndürsün; böylece kullanıcıların yaklaşık
`share_b` yüzdesi B görür. Başlangıç kodunda karşılaştırma ters.

**Beklenen çıktı:**

```text
B
A
```
