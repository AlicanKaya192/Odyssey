A healthcheck says that a service is not just "running" but "able to do its
job". Patterns that help when writing one.

## It can be written in two places

**In compose.yaml** (as in this section), or **in the Dockerfile** with the
`HEALTHCHECK` instruction; then the image itself carries the check and it
applies everywhere:

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health')"
```

If both exist, the one in compose.yaml applies.

## States

| State | Meaning |
|---|---|
| `starting` | Within `start_period`; no decision yet |
| `healthy` | The last tries succeeded |
| `unhealthy` | Failed `retries` times in a row |

`docker ps` and `docker compose ps` print the state: `Up 2 minutes (healthy)`.
The details, with the output of the tries:

```text
docker inspect --format "{{json .State.Health}}" shop-api-1
```

## What should it check?

- For a web service: its own `/health` address; healthy if it returns `200`.
- Keep the `/health` endpoint cheap inside the program: can it connect to the
  database, is the needed file there. Do not do heavy work; it runs every few
  seconds.
- The command runs **inside the container being checked**: `localhost` is the
  right address.

## If there is no `curl`

The `python:3.13-slim` and `alpine` images have no `curl` (alpine has
`wget`). In Python images the easiest is:

```text
python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health')"
```

If the reply is 4xx/5xx or it cannot connect, `urlopen` raises an error and
Python exits with code 1 → the check fails.

## What happens when it is unhealthy?

Docker does **not restart** it by itself; it only reports the state. A
service waiting with `depends_on: condition: service_healthy` does not
start. Large systems (such as Kubernetes) restart an unhealthy container;
Compose on its own does not.
