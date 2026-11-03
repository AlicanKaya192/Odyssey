`hash_pw` ve `DUMMY` hazır. `login(users, user, password)` kullanıcı
varsa ve parolanın özeti kayıtlı özetle `hmac.compare_digest` ile
eşleşiyorsa `"welcome"`, aksi hâlde **her durumda**
`"invalid user name or password"` döndürsün. Bilinmeyen kullanıcıda da
özet hesaplansın: karşılaştırma `DUMMY` ile yapılsın. Başlangıç kodu
farklı mesajlar veriyor.

**Beklenen çıktı:**

```
welcome
invalid user name or password
invalid user name or password
```
