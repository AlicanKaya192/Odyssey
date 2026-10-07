# Introduction to Docker Compose

The command that runs a web application keeps growing:

```text
docker run -d --name web -p 8080:8000 -e APP_ENV=production `
  -e DB_PATH=/data/app.db -v appdata:/data --restart unless-stopped notesapi
```

Writing this correctly every time is hard, it needs to be noted down
somewhere, and if two or three containers have to run together (application
+ database + cache) it gets out of hand. **Docker Compose** gathers all of
this in one file, in a readable form, and runs it with one command.

## The first compose.yaml

In the project folder, next to the `Dockerfile`, a `compose.yaml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8000"
    environment:
      APP_ENV: production
```

- `services:` the list of containers to run. Each is called a **service**;
  here there is one service: `web`.
- `build: .` build the image from the Dockerfile in this folder
  (`docker build .`).
- `ports:` the same as `-p`: `"computer:container"`.
- `environment:` the same as `-e`.

Run it:

```text
docker compose up -d --build
```

```text
 Network notesapi_default Created
 Container notesapi-web-1 Created
 Container notesapi-web-1 Started
```

`up` built the image (`--build`: rebuild if it changed), created a
**network** and started the container in the background (`-d`). In the
browser, `localhost:8080`.

## Where do the names come from?

- **Project name:** the name of the folder containing compose.yaml
  (`notesapi`).
- **Container:** `project-service-number` → `notesapi-web-1`.
- **Image:** `project-service` → `notesapi-web`.
- **Network:** `project_default` → `notesapi_default`. The services see each
  other on this network (the next section).

## Reading YAML

compose.yaml is in **YAML** format: settings nested by indentation.

<figure class="fig">
  <div class="anat">
    <div class="sig"><code>services: / web: / ports: / - "8090:8000"</code></div>
    <div class="anat-row"><span>services:</span><span>The top-level key; no indentation.</span></div>
    <div class="anat-row"><span>  web:</span><span>The service's name; two spaces in. You choose the name.</span></div>
    <div class="anat-row"><span>    ports:</span><span>A setting of web; four spaces in.</span></div>
    <div class="anat-row"><span>      - "8090:8000"</span><span>An item of the list; starts with <code>- </code>, in quotes.</span></div>
  </div>
  <figcaption>Indentation tells what is inside what. Spaces, not tabs.</figcaption>
</figure>

The rules:

- Indentation with **spaces**, not tabs. Lines at the same level start in the
  same column. Usually two spaces.
- `key: value` (a space after the colon).
- A list item starts with `- `.
- Write numbers with a colon such as `"8080:8000"` **in quotes**: in some
  cases YAML can turn values such as `22:22` into a number of minutes.

When the indentation breaks, Compose cannot make sense of it:

```text
go-yaml load error in parser (while parsing a block mapping) at L2.C3-L4.C4:
did not find expected key
```

`L4` → line 4. Odyssey shows the same error with the line number.

## The basic commands

| Command | What does it do? | Single-container equivalent |
|---|---|---|
| `docker compose up -d` | Starts all services in the background | `docker run -d ...` |
| `docker compose up -d --build` | Builds the images first (if needed) | `docker build` + `run` |
| `docker compose ps` | The project's containers | `docker ps` |
| `docker compose logs -f web` | A service's log (live) | `docker logs -f` |
| `docker compose exec web sh` | A command inside a running service | `docker exec -it` |
| `docker compose down` | Removes the containers and the network | `docker rm -f` |
| `docker compose down -v` | Removes the volumes too (**data is lost**) | |
| `docker compose config` | Checks the file and prints its full form | |

`docker compose ps`:

```text
NAME             IMAGE          SERVICE   STATUS          PORTS
notesapi-web-1   notesapi-web   web       Up 2 seconds    0.0.0.0:8080->8000/tcp
```

(We left out the `COMMAND` and `CREATED` columns so it fits.)

`docker compose logs` puts the service's name at the start of each line;
with several services it is clear who wrote what:

```text
web-1  | 172.18.0.1 - - [06/Oct/2026 19:58:57] "GET / HTTP/1.1" 200 -
```

## `docker run` → compose.yaml

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>-p 8080:8000</span><span><code>ports: ["8080:8000"]</code></span></div>
    <div class="anat-row"><span>-e APP_ENV=production</span><span><code>environment: { APP_ENV: production }</code></span></div>
    <div class="anat-row"><span>--env-file .env</span><span><code>env_file: .env</code></span></div>
    <div class="anat-row"><span>-v appdata:/data</span><span><code>volumes: ["appdata:/data"]</code> + <code>volumes: { appdata: }</code> at the bottom</span></div>
    <div class="anat-row"><span>--restart unless-stopped</span><span><code>restart: unless-stopped</code></span></div>
    <div class="anat-row"><span>image name / docker build .</span><span><code>image: ...</code> or <code>build: .</code></span></div>
  </div>
  <figcaption>Every <code>docker run</code> option has a key in compose.yaml.</figcaption>
</figure>

Every part of the long `docker run` command has an equivalent in
compose.yaml:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8000"
    environment:
      APP_ENV: production
      DB_PATH: /data/app.db
    volumes:
      - appdata:/data
    restart: unless-stopped

volumes:
  appdata:
```

- `volumes:` (under the service) is the same as `-v`. If a named volume is
  used, its name is also written under `volumes:` **at the bottom** of the
  file.
- `restart: unless-stopped` restarts the container if it crashes or the
  computer restarts (unless you said `stop`).
- `env_file: .env` environment variables from a file (`--env-file`).
- `image: python:3.13-slim` use a ready-made image instead of building.

## What does `down` remove and what does it leave?

- `docker compose down` removes the containers and the network; **images
  and volumes stay**. The next `up` starts with the same data.
- `docker compose down -v` removes the volumes too: the database is reset.
  Use it on purpose.

## Summary

- Compose gathers all the options of `docker run` in one file
  (`compose.yaml`); the file is kept with the project.
- Each service under `services:`: `build` or `image`, `ports`,
  `environment`, `volumes`, `restart`.
- `docker compose up -d --build` starts, `ps` / `logs` / `exec` watch,
  `down` removes (`-v` together with volumes).
- Names: project = folder, container `project-service-1`, network
  `project_default`.
- YAML: indentation with spaces, `key: value`, list `- `, numbers with a
  colon in quotes. `docker compose config` checks the file.
