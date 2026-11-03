`audit(config)` bir şifreleme yapılandırmasındaki sorunları bu sırayla
listelesin: `mode` `"ECB"` ise `"ecb mode"`, `nonce` `"fixed"` ise
`"fixed nonce"`, `mac` `False` ise `"no integrity"`, `kdf_iterations`
600000'den küçükse `"low iterations"`, `verify_tls` `False` ise `"tls
verification off"`. Başlangıç kodu yalnızca ilk ve son denetimi yapıyor.

**Beklenen çıktı:**

```
[]
fixed nonce
no integrity
low iterations
```
