`state_summary(sizes)` `build(sizes)` ile kurulan modelin state_dict'indeki her
anahtar için `[ad, eleman sayısı]` listesi döndürsün. Eleman sayısı
`tensor.numel()`.

**Beklenen çıktı:**

```
['0.weight', 32]
['0.bias', 8]
['2.weight', 24]
['2.bias', 3]
```
