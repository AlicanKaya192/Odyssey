`d_loss(real_logits, fake_logits, smooth=1.0)` ayırt edicinin kaybını
`BCEWithLogitsLoss` ile hesaplasın: gerçeklerin hedefi `smooth` (etiket
yumuşatma), sahtelerin hedefi 0; iki terimin **toplamı**. 3 basamakla
döndürsün.

**Beklenen çıktı:**

```
1.386
0.605
```
