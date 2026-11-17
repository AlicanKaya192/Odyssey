`vgg_summary(config)` bir listeden VGG tarzı ağ kursun: sayı gördüğünde o
kadar çıkış kanallı `Conv2d(..., 3, padding=1)` + `ReLU`, `"M"` gördüğünde
`MaxPool2d(2)`. İlk giriş 1 kanal. `[parametre sayısı, (1, 1, 16, 16)
girdinin çıktısının yığınsız şekli]` döndürsün.

**Beklenen çıktı:**

```
[16368, [32, 4, 4]]
[1248, [8, 2, 2]]
```
