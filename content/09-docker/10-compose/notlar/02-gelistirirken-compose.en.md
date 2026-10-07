Compose is not only for releases; it is your everyday tool during development
too. A few habits.

## What to do when the code changes?

If you put the code into the image with `COPY`, a change only shows after
rebuilding:

```text
docker compose up -d --build
```

Thanks to the cache only the changed layer is rebuilt; a few seconds.

## Bind mount during development

If you do not want to build on every change, mount the code with a bind
mount:

```yaml
services:
  web:
    build: .
    volumes:
      - ./:/app
```

In Compose, `./` is the folder containing compose.yaml; it works on Windows
too. Editing the code and just restarting the container is enough
(`docker compose restart web`).

## Development and production in separate files

If the same project needs two different setups:

- `compose.yaml`: what is common everywhere.
- `compose.override.yaml`: development only (bind mounts, detailed logs).
  Compose reads this file **automatically** and adds it on top.

To use only the main file in production:
`docker compose -f compose.yaml up -d`.

## One-off commands: `run`

A one-off job in a service's image:

```text
docker compose run --rm web python manage.py migrate
```

`exec` runs in the running container, `run` in a new container (the same
`docker exec` / `docker run` difference).

## Common mistakes

| Symptom | Cause |
|---|---|
| `port is already allocated` | The same port is open in another project or program. |
| `undefined volume` | The named volume is not written under `volumes:` at the bottom. |
| My change does not show | `--build` was forgotten, or the code is copied into the image with `COPY`. |
| `did not find expected key` | The YAML indentation is broken (a tab or a shifted line). |
| The service is `Exited` at once | Look at the last lines with `docker compose logs service`. |

## Cleaning up everything

```text
docker compose down --rmi local -v
```

Containers, the network, the images Compose built and the volumes: the
project starts from scratch. The data goes too; careful.
