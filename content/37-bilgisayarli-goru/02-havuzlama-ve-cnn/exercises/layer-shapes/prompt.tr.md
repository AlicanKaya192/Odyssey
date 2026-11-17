`layer_shapes(size)` dersteki ağın `Flatten`'a kadar olan kısmını kursun:
`Conv2d(1, 8, 3, padding=1)`, `ReLU`, `MaxPool2d(2)`, `Conv2d(8, 16, 3,
padding=1)`, `ReLU`, `MaxPool2d(2)`, `Flatten`. `(1, 1, size, size)`
boyunda sıfır girdiyi katman katman geçirip her katmandan sonraki şekli
(yığın boyutu olmadan) liste olarak toplasın.

**Beklenen çıktı:**

```
[8, 16, 16]
[8, 16, 16]
[8, 8, 8]
[16, 8, 8]
[16, 8, 8]
[16, 4, 4]
[256]
```
