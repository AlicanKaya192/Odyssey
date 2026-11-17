`transfer(state, x, y, x_test, y_test, fine_tune)` kaynak gövdeyi `state`'ten
yüklenmiş yeni bir modeli 10 rakam için eğitip test doğruluğunu döndürsün.
`fine_tune` doğruysa bütün model `lr=0.002` ile, yanlışsa gövde
dondurulup yalnızca baş `lr=0.005` ile eğitilir. İkisinde de Adam, yığın 8,
`generator=torch.Generator().manual_seed(0)`, 30 tur.

**Beklenen çıktı:**

```
True True
True
```
