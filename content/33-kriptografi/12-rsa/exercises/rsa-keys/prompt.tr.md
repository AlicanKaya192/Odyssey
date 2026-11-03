`rsa_keys(p, q, e)` `[n, d]` döndürsün: `n = p * q`, `phi = (p - 1) *
(q - 1)`, `d = pow(e, -1, phi)`. Başlangıç kodu `phi`'yi yanlış
hesaplıyor; `e * d % phi` 1 çıkmıyor.

**Beklenen çıktı:**

```
3233 2753
1
```
