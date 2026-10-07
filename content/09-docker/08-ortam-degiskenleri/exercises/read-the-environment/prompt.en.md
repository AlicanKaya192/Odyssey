`app.py` hard-codes its settings. Make it read them from environment
variables.

**What to do:**

1. Read `env` from the `APP_ENV` variable; if missing, `"development"`.
2. Read `port` from the `PORT` variable; if missing, `8000`. It is used as a
   number (`port + 0`), so `int(...)` is needed.

Odyssey will run the container twice: with no variables and with
`-e APP_ENV=production -e PORT=9000`.

**Expected outputs:**

```
env: development port: 8000
env: production port: 9000
```
