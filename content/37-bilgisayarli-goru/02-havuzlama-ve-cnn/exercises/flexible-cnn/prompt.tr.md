`build_cnn(num_classes)` şu ağı kursun: `Conv2d(1, 16, 3, padding=1)`,
`ReLU`, `MaxPool2d(2)`, `Conv2d(16, 32, 3, padding=1)`, `ReLU`,
`AdaptiveAvgPool2d(1)`, `Flatten`, `Linear(32, num_classes)`.
`param_count(num_classes)` bu ağın parametre sayısını döndürsün. Program
ağı iki farklı boyda resimle dener.

**Beklenen çıktı:**

```
16 (2, 5)
40 (2, 5)
4965
```
