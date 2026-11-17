`evaluate(model, loader, loss_fn)`'i yaz: modeli `eval()` kipine al, `torch.no_grad()`
içinde bütün kümeleri dolaş, `(ortalama kayıp, doğruluk)` döndür. İkisi de örnek
sayısıyla ağırlıklı olmalı (son küme küçük).

**Beklenen çıktı:**

```
0.3858 0.8
```
