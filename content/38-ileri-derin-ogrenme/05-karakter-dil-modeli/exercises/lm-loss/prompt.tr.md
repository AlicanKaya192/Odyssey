`lm_loss(logits, targets)`: `logits` `(B, T, V)`, `targets` `(B, T)`. İkisini
`(B·T, V)` ve `(B·T,)` olarak düzleştirip `nn.functional.cross_entropy` ile
kaybı hesaplasın ve 3 basamakla döndürsün.

**Beklenen çıktı:**

```
1.386
0.0
```
