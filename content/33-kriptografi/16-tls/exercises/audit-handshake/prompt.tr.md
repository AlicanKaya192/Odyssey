`audit_handshake(info)` bir el sıkışmanın özetini (`version`, `suite`,
`cert_ok`, `finished_ok`) denetleyip sorunların listesini döndürsün, bu
sırayla: sürüm `TLSv1.3` ya da `TLSv1.2` değilse `"old version"`, takım
`STRONG_SUITES`'ta değilse `"weak suite"`, sonra `"bad certificate"`,
`"bad finished"`. Başlangıç kodu yalnızca son ikisine bakıyor. Sorun yoksa
boş liste.

**Beklenen çıktı:**

```
[]
old version
weak suite
```
