Compose's default network is enough for most projects. What you need to know
when more is needed.

## Separating networks

The web service should reach the API, the API should reach the database; but
the web service should not reach the database **directly**. With two
networks:

```yaml
services:
  web:
    build: ./web
    networks: [frontend]
  api:
    build: ./api
    networks: [frontend, backend]
  db:
    image: postgres:17
    networks: [backend]

networks:
  frontend:
  backend:
```

`api` is on both networks; `web` and `db` share no network, so they cannot
see each other. Even if an attacker took over the web service, the road to
the database is closed.

## Reaching your computer from a container

Inside a container `localhost` is the container itself. To reach a program
running on your computer (e.g. a database installed outside Docker), Docker
Desktop gives a special name:

```text
http://host.docker.internal:5432
```

On Linux this name does not exist by default; it is added with
`--add-host=host.docker.internal:host-gateway`.

## Network commands

| Command | What does it do? |
|---|---|
| `docker network ls` | Lists networks (`bridge`, `host`, `none` come ready) |
| `docker network create name` | A new network |
| `docker network inspect name` | Connected containers and their addresses |
| `docker network connect name container` | Connects a running container to a network too |
| `docker network rm name` | Removes it (if no container is connected) |
| `docker network prune` | Removes unused networks |

## The ready-made networks

- **bridge**: the network of containers given no `--network`. No name
  resolution; containers cannot find each other by name.
- **host**: the container uses the computer's network directly (on Linux);
  the isolation goes away. Not allowed in Odyssey exercises.
- **none**: no network at all.

## Debugging

If two services cannot reach each other:

1. Are both on the same network? `docker network inspect project_default`.
2. Is the name right? (`api`, not `apii`.)
3. Does the target service listen on `0.0.0.0`? (The Ports section.)
4. Is the target service ready? (`healthcheck`.)
