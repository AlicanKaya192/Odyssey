`both_losses(logits, targets)` iki kaybı döndürsün: doğru kullanım (logits) ve
yanlış kullanım (önce `torch.softmax`, sonra aynı kayıp). İkisi de 3 basamak:
`[doğru, çift softmax]`. Sonuçta yanlış kullanımın neden hep büyük kaldığına
bak.

**Beklenen çıktı:**

```
[0.036, 0.574]
[2.24, 1.38]
```
