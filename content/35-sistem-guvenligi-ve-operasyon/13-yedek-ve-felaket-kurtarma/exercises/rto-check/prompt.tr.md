`rto_check(size_gb, speed, setup, rto)` geri yükleme süresini
`setup + size_gb / speed` ile hesaplasın ve `[sure, tutuyor_mu]`
döndürsün: süre 1 basamağa yuvarlanmış, ikincisi süre `rto`'yu
geçmiyorsa `True`.

**Beklenen çıktı:**

```
[7.5, False]
[2.5, True]
```
