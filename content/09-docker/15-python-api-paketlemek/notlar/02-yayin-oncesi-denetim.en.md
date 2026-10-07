The command to look at for each item of the checklist. The image is
assumed to be named `app` and the container `web` (in Compose,
`docker compose ps` shows the name).

## Image

| Question | Command | Expected |
|---|---|---|
| Is the user not root? | `docker run --rm app id` | `uid=1000(app)` |
| Is the working folder right? | `docker inspect app --format "{{.Config.WorkingDir}}"` | `/app` |
| Are there default settings? | `docker inspect app --format "{{.Config.Env}}"` | `DB_PATH=... PORT=...` |
| Is a health check defined? | `docker inspect app --format "{{json .Config.Healthcheck}}"` | `{"Test":["CMD","python",...` |
| Did `.env` get into the image? | `docker run --rm app ls -a /app` | **no** `.env` |
| Is the size reasonable? | `docker images app` | ~176 MB (`slim` base) |
| How big is each layer? | `docker history app` | Your own layers around KB size |

## Running container

| Question | Command | Expected |
|---|---|---|
| Is it healthy? | `docker ps` | `(healthy)` |
| Why does the check fail? | `docker inspect web --format "{{json .State.Health}}"` | The output of the last checks |
| Can it be reached from outside? | `curl localhost:8095/health` | `{"status": "ok"}` |
| Is the log on the screen? | `docker logs web` | `listening on port 8000...` |
| Does it shut down cleanly? | `docker stop web` then `docker ps -a` | About 1 second, `Exited (0)` |
| Is the data in a volume? | `docker inspect web --format "{{json .Mounts}}"` | `"Type":"volume"`, `/data` |

## Data

```text
docker compose down
docker compose up -d
curl localhost:8095/stats       # the notes are there, starts went up by one
```

If you see `Exited (137)`, the program did not hear SIGTERM and was killed
after 10 seconds: is `CMD` in exec form, is the signal caught?
