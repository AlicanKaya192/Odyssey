Şifre denetimi (`check_password`) ve `bearer = HTTPBearer()` hazır.

**Yapman gerekenler:**

1. `POST /token`: şifre tutmazsa `401` (`"Wrong username or password"`);
   tutarsa `secrets.token_hex(16)` ile jeton üret, `tokens`'a kaydet,
   `{"access_token": ..., "token_type": "bearer"}` döndür.
2. `current_user` bağımlılığı: jeton `tokens`'ta yoksa `401`
   (`"Invalid token"`), varsa kullanıcı adını döndürsün.
3. `GET /me` → `{"user": ...}`.

- `POST /token` `{"username": "ada", "password": "lovelace"}` → jeton
- `GET /me`, `Authorization: Bearer <jeton>` → `{"user": "ada"}`
- `GET /me`, `Authorization: Bearer xyz` → `401`
