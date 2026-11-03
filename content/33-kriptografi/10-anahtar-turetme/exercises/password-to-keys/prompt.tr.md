`hkdf_extract` ve `hkdf_expand` hazır. `keys_from_password(password,
salt_hex, iterations)` bir paroladan şifreleme ve MAC anahtarı türetsin.
Başlangıç kodu parolanın baytlarını doğrudan HKDF'ye veriyor; HKDF hızlı
olduğu için bu parolayı korumaz. Önce yavaş KDF: `master` PBKDF2-SHA256
ile (`salt`, `iterations`, `dklen=32`); sonra aynı tuzla `hkdf_extract` ve
iki etiketle `hkdf_expand`. Sonuç `[enc_hex, mac_hex]`.

**Beklenen çıktı:**

```
False
False
True
```
