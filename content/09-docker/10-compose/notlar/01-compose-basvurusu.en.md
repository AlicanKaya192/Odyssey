The most used keys in compose.yaml and their `docker run` equivalents.

## Service keys

| Key | Example | `docker run` equivalent |
|---|---|---|
| `image` | `image: python:3.13-slim` | `docker run python:3.13-slim` |
| `build` | `build: .` | `docker build .` |
| `container_name` | `container_name: web` | `--name web` |
| `command` | `command: ["python", "app.py"]` | the command after the image (overrides CMD) |
| `entrypoint` | `entrypoint: ["python"]` | `--entrypoint` |
| `ports` | `- "8080:8000"` | `-p 8080:8000` |
| `expose` | `- "8000"` | (only to other services) |
| `environment` | `APP_ENV: production` | `-e APP_ENV=production` |
| `env_file` | `env_file: .env` | `--env-file .env` |
| `volumes` | `- appdata:/data` | `-v appdata:/data` |
| `working_dir` | `working_dir: /app` | `-w /app` |
| `user` | `user: "1000"` | `--user 1000` |
| `restart` | `restart: unless-stopped` | `--restart unless-stopped` |
| `init` | `init: true` | `--init` |
| `depends_on` | `- db` | (start db first) |
| `healthcheck` | `test: [...]` | `--health-cmd` |

## The long form of `build`

```yaml
build:
  context: .
  dockerfile: Dockerfile.dev
  args:
    VERSION: "2.1"
  target: runtime
```

`args` → `--build-arg`, `target` → the stage in a multi-stage build (the
Smaller Images section).

## `environment` can be written two ways

```yaml
environment:
  APP_ENV: production
  DEBUG: "false"
```

```yaml
environment:
  - APP_ENV=production
  - DEBUG=false
```

Both are the same. In the first form, put values such as `true`, `false`,
`yes`, `no` in quotes; YAML may take them as booleans instead of text.

## `restart` options

| Value | When does it restart? |
|---|---|
| `no` (default) | Never |
| `on-failure` | When the program ends with an error (a non-zero code) |
| `always` | Every time it stops (also when Docker restarts) |
| `unless-stopped` | Like `always`, but not if you stopped it |

## The sections at the bottom

```yaml
volumes:
  appdata:

networks:
  backend:
```

**Named** volumes and custom networks used in the services are defined here.
If you use a named volume that is not defined, Compose fails:
`service "web" refers to undefined volume appdata`.

## The file's name

Compose looks for these names in order: `compose.yaml`, `compose.yml`,
`docker-compose.yaml`, `docker-compose.yml`. New projects use
`compose.yaml`. For another name, `docker compose -f file.yaml up`.
