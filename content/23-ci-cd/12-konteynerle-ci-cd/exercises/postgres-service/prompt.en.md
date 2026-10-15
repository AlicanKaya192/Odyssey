The tests want a Postgres database. Add a service to the `test` job:

- Under `services:`, `postgres`: `image: postgres:17`, `POSTGRES_PASSWORD: test` in `env`, a quoted `"5432:5432"` in the `ports` list.
- A health check: `options: >-` with `--health-cmd "pg_isready -U postgres"`, `--health-interval 5s`, `--health-retries 10` under it.
- An environment variable on the test step: `DATABASE_URL: postgresql://postgres:test@localhost:5432/postgres`.
