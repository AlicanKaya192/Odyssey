`step_size(optimizer_class, scale)` `scale · w²` kaybında `w = 1`'den tek bir adım
atıp adımın büyüklüğünü veriyor. `first_step(scale)` `[SGD adımı, Adam adımı]`
döndürsün. Kayıp büyüdükçe SGD'nin adımı büyüyor; Adam'ınki?

**Beklenen çıktı:**

```
0.01 [0.002, 0.1]
1.0 [0.2, 0.1]
100.0 [20.0, 0.1]
```
