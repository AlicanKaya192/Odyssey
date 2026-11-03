`host_matches(pattern, host)` sertifikadaki ad `pattern`'in `host`'u
kapsayıp kapsamadığını döndürsün. Joker (`*.example.test`) **tam bir**
etiketin yerini tutar: `shop.example.test` evet; `a.b.example.test` ve
`example.test` hayır. Joker yoksa ad birebir aynı olmalı. Başlangıç kodu
jokerde yalnızca sona bakıyor.

**Beklenen çıktı:**

```
True
False
True
False
```
