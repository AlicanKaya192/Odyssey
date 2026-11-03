**İmza + sertifika.** `digest` ve `tbs` hazır. `verify_message(cert,
ca_e, ca_n, message, signature)` önce sertifikanın CA tarafından
imzalandığını denetlesin (tutmazsa `"bad certificate"`), sonra mesajın
imzasını **sertifikadaki** açık anahtarla (`cert["e"]`, `cert["n"]`)
doğrulasın (tutmazsa `"bad signature"`); ikisi de tutarsa `"ok"`.
Başlangıç kodu sertifikaya hiç bakmıyor: adı değiştirilmiş bir sertifika
da geçiyor.

**Beklenen çıktı:**

```
ok
bad signature
bad certificate
```
