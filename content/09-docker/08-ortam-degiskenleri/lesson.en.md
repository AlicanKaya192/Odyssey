# Environment Variables and Configuration

The same program runs with different settings in different places: on your
computer it connects to a test database, on the server to the real one;
during development it writes a detailed log, in production a brief one. We do
not want to build a separate image for each place. The way to say **one
image, different settings** is **environment variables**.

## What is an environment variable?

**Name = value** pairs the operating system gives a program when it starts.
The program reads them and adjusts its behaviour. In Python:

```python
import os

env = os.environ.get("APP_ENV", "development")
port = int(os.environ.get("PORT", "8000"))
print("env:", env, "port:", port)
```

- `os.environ.get("NAME", "default")`: the default if the variable is
  missing.
- Values are **always text**; if a number is needed, `int(...)`.

## Giving them when running: `-e`

```text
docker run --rm -e APP_ENV=production -e PORT=9000 app
```

```text
env: production port: 9000
```

The same image prints `env: development port: 8000` without `-e`. The image
did not change; only the settings given to it did.

For many variables, a file (`--env-file`):

```text
# app.env
APP_ENV=staging
DB_HOST=db
```

```text
docker run --rm --env-file app.env app
```

Each line in the file is `NAME=value`; a line starting with `#` is a comment,
no quotes are needed.

`-e NAME` (without a value) passes on the value of the variable with the same
name on your computer. In PowerShell, first `$env:APP_ENV = "test"`, then
`docker run -e APP_ENV app`.

## Putting a default into the image: `ENV`

```dockerfile
ENV APP_ENV=production
ENV PYTHONUNBUFFERED=1
```

`ENV` writes a **default** into the image; it exists in every container run
from that image. A value given with `-e` **overrides** `ENV`:

```text
docker run --rm app                          # env=production (from ENV)
docker run --rm -e APP_ENV=development app   # env=development (-e wins)
```

<figure class="fig">
  <div class="flow">
    <span class="node">The program's default<br><small>os.environ.get(..., "development")</small></span><span class="arrow">←</span>
    <span class="node acc">ENV in the image<br><small>APP_ENV=production</small></span><span class="arrow">←</span>
    <span class="node ok">-e when running<br><small>-e APP_ENV=staging</small></span>
  </div>
  <figcaption>The right one overrides the left: <code>-e</code> if given, otherwise the image's <code>ENV</code>, otherwise the program's own default.</figcaption>
</figure>

Two `ENV` lines often seen in Python images:

| Variable | What does it do? |
|---|---|
| `PYTHONUNBUFFERED=1` | Prints `print` output without holding it back; `docker logs` sees it at once. |
| `PYTHONDONTWRITEBYTECODE=1` | Does not create `__pycache__` / `.pyc` files. |

## Only during the build: `ARG`

`ARG` is a variable valid **only during `docker build`**:

```dockerfile
FROM alpine:3.22
ARG VERSION=1.0
RUN echo "building $VERSION" > /version.txt
```

```text
docker build --build-arg VERSION=2.1 -t app .
```

The `RUN` line sees `2.1`; but **`VERSION` does not exist while the
container runs**:

```text
docker run --rm app sh -c 'echo version=$VERSION'
version=
```

If it is needed while running too, it is passed into `ENV`:
`ENV APP_VERSION=$VERSION`.

| | `ARG` | `ENV` |
|---|---|---|
| When is it valid? | Only during the build | During the build and while running |
| How is it changed? | `--build-arg NAME=value` | `-e NAME=value` |
| Visible in the image? | Yes, in `docker history` | Yes, in `docker image inspect` |

## Secrets go into neither ENV nor ARG

There are two "easy" ways to put a password or an API key into an image; both
are wrong. Let us build with an `ARG` and look at the image's history:

```text
docker build --build-arg TOKEN=s3cret -t app .
docker history app --format "{{.CreatedBy}}"
```

```text
RUN |2 TOKEN=s3cret VERSION=2.1 /bin/sh -c echo "building $VERSION" ...
```

The secret sits **in plain sight** in the image's history. Had we used `ENV`,
`docker image inspect` would show it. Anyone who gets the image can read it.

The right way: **do not put the secret in the image; give it when running.**

- `docker run --env-file secrets.env app` (the file must be in
  `.dockerignore` and `.gitignore`),
- `env_file:` in Compose (the Compose section),
- secret managers in large systems (Docker secrets, the cloud provider's
  secret vault).

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Inside the image</h4><p><code>ENV API_KEY=...</code> → <code>docker image inspect</code> shows it</p><p><code>ARG TOKEN=...</code> → <code>docker history</code> shows it</p><p>Anyone who gets the image reads it</p></div>
    <div class="ok"><h4>When running</h4><p><code>docker run --env-file secrets.env app</code></p><p>The file is in <code>.gitignore</code> and <code>.dockerignore</code></p><p>Sharing the image does not share the secret</p></div>
  </div>
  <figcaption>The rule: a secret is written into no layer of the image.</figcaption>
</figure>

## What goes where?

| Setting | Its place |
|---|---|
| The program's same default everywhere (`PYTHONUNBUFFERED`) | `ENV` |
| What changes with the environment (`APP_ENV`, `DB_HOST`, `PORT`) | `-e` / `--env-file` when running |
| What only affects the build (a version label) | `ARG` |
| Secrets (password, key, token) | Only when running; never in the image |

## Summary

- Environment variables give the program settings from outside; in Python
  `os.environ.get("NAME", "default")`, values are text.
- `-e NAME=value` and `--env-file file` give them when running; `-e`
  overrides the image's `ENV`.
- `ENV` writes a default into the image (valid while running too); `ARG` only
  during the build (`--build-arg`).
- **A secret does not go into the image:** an `ARG` value shows in
  `docker history`, an `ENV` value in `docker image inspect`. Secrets are
  given when running.
