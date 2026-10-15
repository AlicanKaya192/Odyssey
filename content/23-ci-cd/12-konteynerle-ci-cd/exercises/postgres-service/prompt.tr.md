Testler bir Postgres veritabanı istiyor. `test` işine bir servis ekle:

- `services:` altında `postgres`: `image: postgres:17`, `env` içinde `POSTGRES_PASSWORD: test`, `ports` listesinde tırnaklı `"5432:5432"`.
- Sağlık denetimi: `options: >-` ve altında `--health-cmd "pg_isready -U postgres"`, `--health-interval 5s`, `--health-retries 10`.
- Test adımına ortam değişkeni: `DATABASE_URL: postgresql://postgres:test@localhost:5432/postgres`.
