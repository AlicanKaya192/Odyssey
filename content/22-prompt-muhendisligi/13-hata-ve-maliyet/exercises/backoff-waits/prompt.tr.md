`backoff_waits(attempts, base, cap)` `attempts` denemenin arasındaki
bekleme sürelerini liste olarak döndürsün: `attempts - 1` bekleme,
`i`'nci bekleme `base * 2 ** i`, ama hiçbiri `cap`'ten büyük olmasın.

**Beklenen çıktı:**

```
[1.0, 2.0, 4.0]
[0.5, 1.0, 2.0, 4.0, 8.0, 8.0]
[]
```
