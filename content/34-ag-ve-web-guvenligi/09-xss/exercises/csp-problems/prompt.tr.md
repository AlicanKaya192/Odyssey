`csp_problems(header)` bir CSP değerini denetleyip sorun kodlarını
**şu sırayla** bir liste olarak döndürsün. Betik kaynakları `script-src`'den,
o yoksa `default-src`'den okunur. İkisi de yoksa yalnızca
`["no-script-src"]`. Kaynaklarda `'unsafe-inline'` varsa `"unsafe-inline"`,
`*` varsa `"wildcard"`. Yönergeler `;` ile ayrılır, ilk kelime yönergenin
adıdır.

**Beklenen çıktı:**

```
[]
['unsafe-inline']
['no-script-src']
['wildcard']
```
