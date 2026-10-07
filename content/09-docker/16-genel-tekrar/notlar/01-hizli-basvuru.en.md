All the commands and rules of the track on one page.

## Container

```text
docker run --rm -it python:3.13-slim sh      # open, go inside, remove when done
docker run -d --name web -p 8080:8000 app    # in the background, port open
docker ps -a                                 # all of them, with exit codes
docker logs -f --tail 50 web                 # the log (live)
docker exec -it web sh                       # inside a running container
docker stop web && docker rm web             # stop, remove
docker cp web:/app/log.txt .                 # take a file out
```

## Image

```text
docker build -t app .                        # build from this folder
docker build --no-cache --progress=plain -t app .
docker images                                # images and their sizes
docker history app                           # layers
docker image prune                           # remove untagged images
```

## Dockerfile

| Instruction | Note |
|---|---|
| `FROM python:3.13-slim` | A pinned version; a stage name with `AS build` |
| `WORKDIR /app` | Creates the folder and moves there |
| `COPY requirements.txt .` | Dependencies first |
| `RUN pip install --no-cache-dir -r ...` | Commands in one layer with `&&` |
| `COPY . .` | Code last; with `.dockerignore` |
| `ENV KEY=value` | A default setting; not a secret |
| `USER app` | After the packages |
| `EXPOSE 8000` | Documentation |
| `HEALTHCHECK CMD [...]` | 0 healthy, 1 unhealthy |
| `CMD ["python", "app.py"]` | Exec form |
| `COPY --from=build ...` | Multi-stage build |

## Data and settings

```text
docker run -v notes:/data app                # named volume
docker run -v ${PWD}:/app app                # bind mount (PowerShell)
docker run -e DEBUG=1 --env-file .env app    # environment variables
docker volume ls / docker volume rm notes
```

## Compose

```text
docker compose up -d --build                 # build and start
docker compose ps                            # state, (healthy)
docker compose logs -f web                   # one service's log
docker compose exec web sh                   # inside the service
docker compose down                          # remove (the volume stays)
docker compose down -v                       # together with the volumes
```

## Exit codes

| Code | Meaning |
|---|---|
| `0` | The program finished its job |
| `1` | The program's own error (`docker logs`) |
| `127` | Command not found (the spelling in `CMD`) |
| `137` | Killed: SIGTERM not heard, or memory |
| `143` | Shut down by SIGTERM (with `--init`) |

## Keep in mind

> The Dockerfile is the recipe, the image the class, the container the
> object. Packages first, then code. Data in a volume, settings in the
> environment, secrets nowhere. The program on `0.0.0.0`, without root, in
> exec form.
