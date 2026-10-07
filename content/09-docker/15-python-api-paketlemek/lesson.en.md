# Packaging a Python API

In this section we bring everything you have learned on this track
together in one real project: we prepare a small notes API (a server that
programs talk to over HTTP) for Docker from start to finish. At the end you
will have a service that starts on another computer with a single command,
does not lose its data, does not run as root and reports its own health.

## The project

```text
notes-api/
├── app.py            # the API itself
├── healthcheck.py    # the "am I healthy?" check
├── requirements.txt  # Python packages
├── Dockerfile
├── .dockerignore
├── compose.yaml
└── .env              # settings that change per environment
```

The API offers three addresses:

| Request | What does it do? |
|---|---|
| `GET /health` | `{"status": "ok"}`: is the program up? |
| `GET /notes` / `POST /notes` | Lists the notes / adds a new note. |
| `GET /stats` | The number of notes and how many times the program has started. |

The notes live in an SQLite database (a single-file database). The program
only uses Python's standard library, so `requirements.txt` is empty for
now, but the structure will stay the same on the day a package is added.

<figure class="fig">
  <div class="flow">
    <span class="node">curl<br><small>localhost:8095</small></span><span class="arrow">→</span>
    <span class="node">ports<br><small>8095 → 8000</small></span><span class="arrow">→</span>
    <span class="node ok">app.py<br><small>0.0.0.0:8000, USER app</small></span><span class="arrow">→</span>
    <span class="node acc">notes-data<br><small>/data/notes.db</small></span>
  </div>
  <figcaption>The path of a request: from the computer's port to the container, from the program to the database in the volume. Even if the container is removed, the database stays in the volume.</figcaption>
</figure>

## Is the program ready for Docker?

Before writing a Dockerfile, the program itself must follow four rules.
You have seen all of them in earlier sections; here we look at how they
appear in `app.py`.

**1. Listen on every address.** `localhost` means only the container
itself; a request from outside cannot reach it (the Ports section).

```python
ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
```

**2. Read settings from the environment.** The database location and the
port are not written into the code; they have defaults, and an environment
variable wins if it exists (the Environment Variables section).

```python
DB_PATH = os.environ.get("DB_PATH", "notes.db")
PORT = int(os.environ.get("PORT", "8000"))
```

**3. Write the log to the screen.** Not to a file, to standard output:
`docker logs` collects it. `flush=True` (or `PYTHONUNBUFFERED=1` in the
image) makes the line come out without waiting.

**4. Shut down cleanly on SIGTERM.** `docker stop` first sends SIGTERM and
kills after 10 seconds (the CMD and ENTRYPOINT section). A program that
catches the signal shuts down at once and cleanly:

```python
def stop(signum, frame):
    print("shutting down", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, stop)
```

We measured it: with this program `docker compose stop` finished in
**0.9 seconds** and the exit code was 0.

## The Dockerfile, line by line

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/notes.db \
    PORT=8000

RUN useradd --create-home --uid 1000 app \
 && mkdir /data \
 && chown app:app /data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py healthcheck.py ./

USER app
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python", "healthcheck.py"]
CMD ["python", "app.py"]
```

| Line | Why? |
|---|---|
| `FROM python:3.13-slim` | A small base image with a pinned version. |
| `PYTHONDONTWRITEBYTECODE=1` | Python should not write `__pycache__` files; they are useless in a container. |
| `PYTHONUNBUFFERED=1` | Output should reach `docker logs` without waiting. |
| `DB_PATH`, `PORT` | Default settings; they can be changed at run time. |
| `useradd ... && mkdir /data && chown` | Prepare the user and the data folder **in one layer**; the folder belongs to the user. |
| `COPY requirements.txt` → `RUN pip install` | Packages first: when the code changes, these layers come from the cache. |
| `COPY app.py healthcheck.py ./` | The often-changing code last. With several files, the destination ends with `./`. |
| `USER app` | The program runs without root; **after** installing packages. |
| `EXPOSE 8000` | Documentation: the program listens on this port. |
| `HEALTHCHECK` | Docker checks the program's health itself. |
| `CMD [...]` | Exec form: SIGTERM reaches Python directly. |

The built image is **176 MB** on disk (43 MB compressed when downloaded);
almost all of it is the base image. The layers we added come to about
115 KB in total (measured with `docker history`).

## `HEALTHCHECK`: Docker's own check

In the Compose section we wrote the health check into `compose.yaml`. The
`HEALTHCHECK` instruction puts the same thing **inside the image**: whoever
runs the image, however they run it, the check comes along.

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python", "healthcheck.py"]
```

- `--interval=5s`: check every 5 seconds (the default is 30 seconds).
- `--timeout=3s`: count it as failed if no answer comes in 3 seconds.
- `--retries=3`: call it "unhealthy" after 3 failures in a row.
- `CMD`: the check command. Exit code 0 → healthy, 1 → unhealthy.

The check command runs **inside** the container. `python:3.13-slim` has no
`curl`, so we wrote the check in Python in a separate file:

```python
PORT = os.environ.get("PORT", "8000")

try:
    urllib.request.urlopen(f"http://localhost:{PORT}/health", timeout=2)
except OSError:
    sys.exit(1)
```

The port is read from the environment: if someone changes `PORT`, the check
changes with it. Do not forget that the check file must be copied into the
image.

```text
docker compose ps
NAME             STATUS
notesapi-web-1   Up 2 seconds (health: starting)
notesapi-web-1   Up 6 seconds (healthy)
```

Until the first check passes the state is `health: starting`, then
`healthy`. When we deliberately pointed the check at the wrong port (9000),
the container kept running but became `(unhealthy)` after about 15
seconds: 3 failures in a row at a 5-second interval.

## `.dockerignore`

```text
.git
.env
**/__pycache__
*.db
```

- `.env` must not enter the image: its settings (later, passwords) should
  not travel to everyone with the image.
- `*.db`: the database created while you test on your computer should not
  be copied into the image; the data lives in the volume.

## `compose.yaml`

```yaml
services:
  web:
    build: .
    ports:
      - "8095:8000"
    env_file: .env
    volumes:
      - notes-data:/data
    restart: unless-stopped

volumes:
  notes-data:
```

| Setting | What does it do? |
|---|---|
| `build: .` | Build the image from the Dockerfile in this folder. |
| `ports` | The computer's 8095 to the container's 8000. |
| `env_file: .env` | Take environment variables from a file; they override the Dockerfile's `ENV`. |
| `notes-data:/data` | A named volume: the database stays even if the container is removed. |
| `restart: unless-stopped` | Restart the program if it crashes; not if you stopped it. |

`.env`:

```text
DB_PATH=/data/notes.db
PORT=8000
```

The `ENV` in the Dockerfile is the **default**, `.env` is that
environment's setting. The same image can run with a different `.env` on a
development computer and on a server.

## Running and trying it

```text
docker compose up -d --build
curl localhost:8095/health
{"status": "ok"}
```

To add a note, write the body to a file (`note.json`: `{"text": "buy milk"}`)
and send it with `-d @file`; you do not have to escape quotes in the shell.
In PowerShell `curl` is an alias of another command; write `curl.exe` there.

```text
curl -X POST localhost:8095/notes -d @note.json
{"id": 1, "text": "buy milk"}
curl localhost:8095/notes
[{"id": 1, "text": "buy milk"}]
```

When you send an empty note the program rejects it with `400`:
`{"error": "text is required"}`. The log:

```text
docker compose logs web
web-1  | listening on port 8000, database /data/notes.db
web-1  | POST /notes 201
web-1  | POST /notes 400
web-1  | GET /notes 200
```

The health check sends a request to `/health` every 5 seconds; the program
does not log that address so that it does not fill the log.

## Is the data permanent?

```text
docker compose down
docker compose up -d
curl localhost:8095/stats
{"notes": 1, "starts": 2}
```

`down` removed the container and `up` created a new one; the note is still
there and the program knows it has started a second time, because the
database is in the volume. `docker compose down -v`, however, removes the
volume too: the data is gone.

Looking from inside the container, the file belongs to the user (1000):

```text
docker compose exec web ls -ln /data
-rw-r--r-- 1 1000 1000 12288 Oct  6 20:34 notes.db
```

## Common mistakes

**The data folder is not given to the user.** Without the
`mkdir /data && chown app:app /data` line the program fails as soon as it
starts:

```text
sqlite3.OperationalError: unable to open database file
```

An empty named volume takes the owner its folder has in the image. If the
folder does not exist in the image at all, Docker creates it owned by root
and the `app` user cannot write there.

**The health check is not copied or looks at the wrong port.** The program
runs, but after a while the state becomes `unhealthy`. The reason is in the
output of `docker inspect web --format "{{json .State.Health}}"`, in the
last outputs of the check.

**Listening on `localhost`.** The port looks open but the request gets no
answer (`Empty reply from server`); the program must listen on `0.0.0.0`.

**Changing the code and not rebuilding.** `docker compose up -d` does not
rebuild the image; if the code changed, use `--build`.

## A checklist before shipping

1. The program listens on `0.0.0.0`, reads its settings from the
   environment, writes its log to the screen and shuts down on SIGTERM.
2. The base image's version is pinned (`python:3.13-slim`).
3. First `requirements.txt` and `pip install`, then the code.
4. There is a `.dockerignore`; `.env` and the local database do not enter
   the image.
5. The user is `USER app`; the folders written to belong to it.
6. `EXPOSE`, `HEALTHCHECK` and `CMD` in exec form.
7. The data is in a named volume; `restart: unless-stopped`.
8. `docker compose up -d --build` → `healthy` → requests are answered →
   the data is still there after `down` / `up`.

## Summary

- The program must be ready first: `0.0.0.0`, environment variables, a log
  on the screen, SIGTERM.
- In the Dockerfile the order matters for the cache (packages first, code
  last), for security (`USER` after the packages) and for shutting down
  (exec form).
- `HEALTHCHECK` puts the health check inside the image; the check runs
  inside the container, exit code 0 = healthy.
- Compose sets up the service with one command; the data is in a named
  volume, the settings in `.env`.
