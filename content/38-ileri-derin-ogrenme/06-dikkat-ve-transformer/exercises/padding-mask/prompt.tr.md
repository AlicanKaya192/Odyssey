`padding_mask(ids, pad)` `key_padding_mask` olarak verilebilecek maskeyi
döndürsün: dolgu kimliğinin (`pad`) olduğu yerde `True`, gerçek kimlikte
`False`.

**Beklenen çıktı:**

```
[False, False, True, True]
[False, False, False, True]
```
