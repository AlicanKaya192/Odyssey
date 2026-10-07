# Overall Review

You have reached the end of the Docker track. You started with the "it
worked on my machine" problem; now you can turn a Python program into a
service that runs the same on every computer, keeps its data, does not run
as root and reports its health. This section walks the road from start to
finish once more: at each stop, the most important idea and the command you
will use most.

<figure class="fig">
  <div class="flow">
    <span class="node">Basics<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">Dockerfile<br><small>04–06</small></span><span class="arrow">→</span>
    <span class="node">Data, Compose<br><small>07–11</small></span><span class="arrow">→</span>
    <span class="node">Safe<br><small>12–14</small></span><span class="arrow">→</span>
    <span class="node acc">API<br><small>15</small></span>
  </div>
  <figcaption>The road of the Docker track: from a single container to a service that runs the same on every computer.</figcaption>
</figure>

## 1. Container and image (Sections 00–03)

An **image** is a frozen package of a program and everything it needs; a
**container** is a running copy opened from that image. You can open as many
containers from one image as you like. A container is not a virtual
machine: it does not boot its own operating system, it shares the
computer's kernel; that is why it starts in a second.

```text
docker run --rm python:3.13-slim python -c "print(42)"
docker run -d --name web python:3.13-slim sleep 300
docker ps -a / docker logs web / docker exec -it web sh
docker stop web / docker rm web
```

An image is made of **layers**; images that use the same base image share
those layers. A name without a tag means `latest`; always write the version
(`python:3.13-slim`).

## 2. Dockerfile (Sections 04–06)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

- Every instruction is a layer; everything **after** a changed instruction
  does not come from the cache. That is why packages come first and the
  often-changing code last.
- `.dockerignore` filters out what should not enter the context: `.git`,
  `.venv`, `**/__pycache__`, `.env`.
- `CMD` is the default command, overridden by `docker run app ...`.
  `ENTRYPOINT` is the fixed command and `CMD` becomes its arguments.
- **Exec form** (`["python", "app.py"]`): SIGTERM reaches the program. In
  shell form `docker stop` waits 10 seconds and kills (`137`).

## 3. Connecting to the outside (Sections 07–09)

| Topic | Rule |
|---|---|
| Port | `-p 8080:8000`: the computer's 8080 → the container's 8000. The program must listen on `0.0.0.0`. |
| Environment | `-e KEY=value`, `--env-file .env`; `ENV` in the Dockerfile is the default. Secrets do not go into the image. |
| Volume | `-v notes:/data`: the data is outside the container and stays even if the container is removed. |
| Bind mount | `-v ${PWD}:/app`: a folder on your computer inside the container; for development. |

The file system inside the container is temporary: when the container is
removed, everything written into it is gone. Everything that must stay goes
into a volume.

## 4. Compose (Sections 10–11)

```yaml
services:
  web:
    build: ./web
    ports: ["8095:8000"]
    env_file: .env
    depends_on:
      api:
        condition: service_healthy
  api:
    build: ./api
    volumes: [api-data:/data]
    healthcheck:
      test: ["CMD", "python", "healthcheck.py"]
volumes:
  api-data:
```

Compose gathers all the `docker run` settings in one file:
`docker compose up -d --build`, `ps`, `logs -f`, `down` (`-v` also removes
the volumes). The services are on the same network and reach each other
**by service name** (`http://api:8000`); inside a container `localhost` is
the container itself. `depends_on` is only the start order; for "wait until
it is ready", a health check + `condition: service_healthy`.

## 5. A production-ready image (Sections 12–13)

- **Multi-stage build:** the build tools stay in the first stage and only
  the result is copied into the final image (`COPY --from=build`). In the
  example we measured, 176 MB → 12.8 MB.
- Deleting a file in a later `RUN` does not make the image smaller: the
  file is still in the earlier layer. Download, use and delete in the same
  `RUN`.
- **Do not be root:** `RUN useradd ... app` + `USER app`; give the folders
  written to the user with `chown`.
- Secrets do not go into the image (even `ARG` values show in
  `docker history`); no `--privileged` and no mounting the Docker socket.

## 6. When something goes wrong (Section 14)

First decide which phase it is in:

| The image cannot be built | The container does not work |
|---|---|
| The **last lines** of the output | `docker ps -a` → exit code |
| The failing step `[3/5] RUN ...` | `docker logs` → last words |
| `--progress=plain --no-cache` | Look inside with `--entrypoint sh` |

Exit codes: `0` the job is done (natural if it is not a server), `1` the
program's error, `127` command not found, `137` killed (SIGTERM not heard,
or memory).

## All the pieces together (Section 15)

The Dockerfile from the track's final project uses almost every section:

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

A pinned base (03), cache order (05), settings from the environment (08), a
data folder (09), a non-root user (13), a health check (11, 15), exec form
(06). If you can say why each line is there, you have reached the goal of
this track.

## What comes next?

Docker taught you to **package** and **run** a program. The next step is to
take the API you write (the API 2 track) or a machine learning model to a
server in this package: the same image, the same `compose.yaml`, only a
different `.env`.
