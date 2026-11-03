Kayıt biçimi `pbkdf2_sha256$tekrar$tuz$anahtar`. `make_record` hazır.
`upgrade(password, record, minimum)` parolayı kayıttaki parametrelerle
doğruluyor; yanlışsa `"wrong password"` dönüyor. Eksik olan: parola
doğruysa ve kayıttaki tekrar sayısı `minimum`'dan **küçükse** aynı tuzla
ve `minimum` tekrarla yeni bir kayıt döndürsün; değilse kaydı olduğu gibi
versin.

**Beklenen çıktı:**

```
3000
True
wrong password
```
