`redact(line)` kayıt satırındaki `password`, `token`, `secret` ve
`api_key` alanlarının değerini `***` yapsın; anahtar adı olduğu gibi
kalsın. Büyük-küçük harf fark etmez (`Token=...` da gizlenir). Değer, `=`
işaretinden sonraki boşluğa kadar olan kısımdır.

**Beklenen çıktı:**

```
login user=ada password=*** ok
api_key=*** Token=*** status=200
nothing to hide here
```
