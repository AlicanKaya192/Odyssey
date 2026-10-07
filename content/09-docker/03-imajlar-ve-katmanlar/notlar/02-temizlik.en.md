As you work with Docker, images, stopped containers and the build cache pile
up. First look at how much space they take, then remove only what is needed.

## How much space do they take?

```text
docker system df
```

```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          2         0         191.2MB   191.2MB (99%)
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     20        0         60.85MB   14MB
```

- **ACTIVE**: what a container is using right now.
- **RECLAIMABLE**: the space freed if removed.

## Clean-up commands, from small to large

| Command | What does it remove? |
|---|---|
| `docker rm name` | A single container |
| `docker rmi image:tag` | A single image (or only one of its names) |
| `docker container prune` | All **stopped** containers |
| `docker image prune` | **Nameless** (`<none>`) images |
| `docker image prune -a` | **All** images no container uses |
| `docker builder prune` | The build cache |
| `docker volume prune` | Unused volumes (**data is lost**) |
| `docker system prune` | Stopped containers + nameless images + idle networks + cache |

All of them tell you what they will do and ask for `y/N` confirmation before
removing. With `-f` they do not ask; that is used in scripts, there is no
need for it when typing by hand.

## Things to watch

- **`volume prune` removes data.** If a database's data is in a volume, it
  does not come back. Do not touch it until the Volumes section.
- **`image prune -a`** removes all unused images; `python:3.13-slim` may go
  too and will be downloaded again on the next build (internet needed).
- **Odyssey's images** are called `odyssey-ex-...`. Removing them from
  Settings › Docker is safer: it only touches what Odyssey marked.

## A habit

Looking at `docker system df` once a week is enough. If you run trial
containers with `--rm`, stopped containers do not pile up in the first place.
