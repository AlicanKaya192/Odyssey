**Yapman gerekenler:**

1. `UserIn` (`name`, `password`) ve `UserOut` (`id`, `name`) modelleri.
2. `POST /users`: kaydı `users` sözlüğüne **şifresiyle birlikte** koy, `201`
   ile döndür; cevapta şifre olmasın.
3. `GET /users`: bütün kullanıcıların listesi, yine şifresiz.

- `POST /users`, `{"name": "Ada", "password": "s3cret"}` → `201`, `{"id": 1, "name": "Ada"}`
- `GET /users` → `[{"id": 1, "name": "Ada"}]`
