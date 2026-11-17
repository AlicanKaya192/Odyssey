`by_hand(x)` eğitim kipindeki `nn.BatchNorm1d`'nin yaptığını elle yapsın: her
sütundan sütunun ortalamasını çıkar, `sqrt(varyans + 1e-5)`'e böl. Varyans
yanlılı (`unbiased=False`). Doğruysa `check_batchnorm` `True` basar.

**Beklenen çıktı:**

```
True
```
