`ResidualBlock.forward`'ı yaz: `out = ReLU(bn1(conv1(x)))`,
`out = bn2(conv2(out))`, sonuç `ReLU(out + x)`. Program bir de `bn2`'nin
ölçeğini sıfırlayınca bloğun `ReLU(x)`'e dönüştüğünü sınar: artık yol
kalınca blok girdiyi olduğu gibi geçirebiliyor.

**Beklenen çıktı:**

```
(2, 4, 6, 6)
True
```
