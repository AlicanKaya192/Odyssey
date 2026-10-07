**Yapman gereken:** `Signup` modeline iki doğrulayıcı yaz.

- `username`: yalnızca harf ve rakam (`str.isalnum()`); geçerliyse **küçük
  harfe** çevrilmiş hâli kalsın.
- `email`: içinde `@` olmalı.
- `POST /signup` modeli olduğu gibi döndürsün.

- `{"username": "AdaL99", "email": "ada@example.com"}` → `{"username": "adal99", "email": "ada@example.com"}`
- `{"username": "ada l", "email": "ada@example.com"}` → `422`
- `{"username": "ada", "email": "ada.example.com"}` → `422`
