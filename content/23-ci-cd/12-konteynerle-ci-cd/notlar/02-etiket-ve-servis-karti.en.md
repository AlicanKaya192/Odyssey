**Which tag when?**

| When | Tag | Does it change? |
|---|---|---|
| On every build | The commit id (`4f2a9c8`) | No |
| On a push to `main` | `latest` | Yes, on every push |
| On a `v1.4.2` tag | `1.4.2` and `1.4` | `1.4.2` no, `1.4` yes |

- Deploy with a tag that **does not change** (the SHA or the full
  version). A server deployed with `latest` cannot be taken back to "the
  previous one".
- Do not give `latest` to a branch build.

**The layer cache**

- When a step changes, that step and **every step after it** run again.
- The pipeline's machine starts from scratch every time: the cache comes
  with `cache-from` / `cache-to`.
- In the Dockerfile the file that changes often goes last:

```text
FROM python:3.13-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**A service: a database next to the job**

```yaml
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_PASSWORD: test
        ports:
          - "5432:5432"
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 5s
          --health-retries 10
```

| Part | Why |
|---|---|
| `ports` | The tests connect to `localhost:5432` |
| Health check | So the tests do not start before the database is ready |
| Quoted port | Values like `22:22` become base-60 numbers in some readers |
| Plain password | Not a problem: the database exists only during this job |

**Common mistakes**

| Symptom | Cause |
|---|---|
| `docker run` cannot find the image | `load: true` is missing |
| The push gives a permission error | No `packages: write` permission |
| The push gives a name error | Capital letters in the image name |
| Tests sometimes cannot connect | No health check on the service |
| Every build takes minutes | No cache, or `COPY . .` before the install |
