`users` sözlüğünde şifreler değil, **özetleri** duruyor (tuz `SALT`).

**Yapman gerekenler:**

1. `hash_password(password, salt)`:
   `hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()`.
2. `POST /login` (`username`, `password`): gelen şifrenin özeti
   saklananla eşitse `{"ok": true, "user": ...}`; değilse ya da kullanıcı
   yoksa `401`, `"Wrong username or password"`. Karşılaştırma
   `hmac.compare_digest`.

- `{"username": "ada", "password": "lovelace"}` → `{"ok": true, "user": "ada"}`
- `{"username": "ada", "password": "enigma"}` → `401`
- `{"username": "bob", "password": "x"}` → `401`, aynı mesaj
