Başlangıç kodu bir kodlayıcı, bir konum gömmesi (`pos`), bir girdi `x` ve
diziyi ters çeviren `perm` kuruyor. `position_matters(length)` iki değer
döndürsün (`torch.no_grad()` içinde, `atol=1e-5` ile `torch.allclose`):

- `plain`: `encoder(x)[:, perm]` ile `encoder(x[:, perm])` aynı mı?
- `positioned`: aynı soru, ama kodlayıcıya `x + pos.weight` ve
  `x[:, perm] + pos.weight` verilince.

**Beklenen çıktı:**

```
[True, False]
[True, False]
```
