`gan_losses(real_logits, fake_logits)` iki kaybı `BCEWithLogitsLoss` ile
hesaplasın: ayırt edici (gerçeklere 1, sahtelere 0, toplam) ve üretici
(sahtelere 1). 3 basamakla liste döndürsün.

**Beklenen çıktı:**

```
[1.386, 0.693]
```
