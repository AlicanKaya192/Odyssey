`bucket(user_id, salt)` `f"{salt}:{user_id}"` metninin MD5 özetini
(`hashlib.md5(...).hexdigest()`) 16 tabanında sayıya çevirip 100'e bölümünden
kalanı döndürsün. Başlangıç kodu harf kodlarını topluyor; benzer kimlikler
benzer kovalara düşer.

**Beklenen çıktı:**

```text
41
60
```
