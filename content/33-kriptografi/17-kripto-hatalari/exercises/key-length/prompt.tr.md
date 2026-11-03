`check_key(algorithm, bits)` `"ok"` ya da `"too short"` döndürsün:
`rsa` için en az 2048, `aes` için yalnızca 128, 192 ya da 256, `ec` için en
az 256. Bilinmeyen algoritma `"unknown"`. Başlangıç kodu yalnızca RSA'ya
bakıyor ve geri kalan her şeyi kabul ediyor.

**Beklenen çıktı:**

```
too short
too short
ok
unknown
```
