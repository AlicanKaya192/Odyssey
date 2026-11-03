`check_pair(e, d, n, samples)` bir anahtar çiftinin doğru olup
olmadığını sınasın: `samples`'taki her `m` için `pow(pow(m, e, n), d, n)
== m` olmalı; biri bile tutmazsa `False`. Başlangıç kodu `e * d % n`'e
bakıyor; ama ters `n`'e göre değil `phi`'ye göre alınır, doğru çift bile
reddediliyor.

**Beklenen çıktı:**

```
True
False
```
