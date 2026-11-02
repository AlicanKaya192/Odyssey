`lookalike(domain, trusted)` bir alan adının güvenilen alan adına **benzer
görünen ama farklı** bir taklit olup olmadığını söylesin.

Karışan karakterleri tek biçime getiren bir `normalize` yaz: önce küçük
harf, sonra şu değiştirmeler bu sırayla: `"rn"` → `"m"`, `"vv"` → `"w"`,
`"0"` → `"o"`, `"1"` → `"l"`.

İki adın normalize hâli **aynı** ama kendileri (küçük harfle) **farklıysa**
`True`. Aynı alan adı taklit değildir.

**Beklenen çıktı:**

```
examp1e.com True False
example.com False False
exarnple.com True False
vvebsite.test False True
other.com False False
```
