**What to do:** write two validators on the `Signup` model.

- `username`: letters and digits only (`str.isalnum()`); if valid, keep it
  **lower-cased**.
- `email`: must contain `@`.
- `POST /signup` returns the model as it is.

- `{"username": "AdaL99", "email": "ada@example.com"}` → `{"username": "adal99", "email": "ada@example.com"}`
- `{"username": "ada l", "email": "ada@example.com"}` → `422`
- `{"username": "ada", "email": "ada.example.com"}` → `422`
