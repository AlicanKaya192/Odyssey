`after_decay(start, lr, decay, steps)` gradyanı hep 0 olan bir kayıpla (`w · 0`)
`SGD(lr, weight_decay=decay)` ile `steps` adım atsın ve son ağırlığı 4 basamakla
döndürsün. Sonuç `start · (1 − lr · decay)^steps` olmalı.

**Beklenen çıktı:**

```
0.9703
1.62
```
