# Security and Good Habits

A container separates a program from the rest of the computer, but the
separation is not absolute: the kernel is shared, some settings loosen the
separation, and whatever you put into the image by mistake travels to
everyone with the image. In this section we gather the most important habits;
you saw most of them in earlier sections, now together and with their
reasons.

## A container is root by default

```text
docker run --rm python:3.13-slim id
uid=0(root) gid=0(root) groups=0(root)
```

The program inside the container runs as **root** (the administrator, user
number 0). If the program is taken over, the attacker can do anything inside
the container; they can write to a mounted folder as root; if there is a hole
in the kernel, the chance of getting out grows.

The rule: **run the program as a non-root user.**

## `USER`: switching to a user

```dockerfile
FROM python:3.13-slim
RUN useradd --create-home --uid 1000 app
WORKDIR /app
COPY . .
USER app
CMD ["python", "app.py"]
```

- `useradd --create-home --uid 1000 app`: create a user called `app` with a
  home folder and the number 1000 (in Debian-based images; on Alpine
  `adduser -D app`).
- `USER app`: the instructions after this line **and the container itself**
  run as this user.

```text
docker run --rm app id
uid=1000(app) gid=1000(app) groups=1000(app)
```

Write `USER` **after** installing packages: `pip install` and `apt-get` need
root.

## The permission trap

`WORKDIR /app` creates the folder as root. After `USER app`, when the program
tries to write there:

```text
touch: cannot touch '/app/x': Permission denied
```

Reading is allowed, writing is not. If the program will write to a folder,
make the user its owner:

```dockerfile
RUN useradd --create-home --uid 1000 app
WORKDIR /app
RUN chown app:app /app
USER app
```

Copied files are also owned by root by default; if needed,
`COPY --chown=app:app . .`. If data is written to a volume (the Volumes
section), the folder the volume is mounted on (`/data`) is given to the user
the same way.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>As root (the default)</h4><p>uid=0</p><p>If taken over, anything goes in the container</p><p>Writes to mounted folders as root</p></div>
    <div class="ok"><h4>USER app</h4><p>uid=1000</p><p>Can write only to its own folder</p><p>The damage stays limited</p></div>
  </div>
  <figcaption>Install packages as root, run the program as a user: <code>USER</code> comes after installing packages.</figcaption>
</figure>

## Reducing privileges when running

| Option | What does it do? |
|---|---|
| `--read-only` | Makes the container's file system read-only; places to write are given with volumes. |
| `--cap-drop ALL` | Removes root's special powers (network settings, changing file ownership...). |
| `--memory 512m --cpus 1` | A memory and processor limit; a runaway program does not lock up the computer. |
| `--user 1000` | Runs as a user even if the image has no `USER`. |

```text
docker run --rm --read-only alpine:3.22 sh -c "touch /x"
touch: /x: Read-only file system
```

Things **never** done:

- `--privileged`: gives the container almost all of the computer's powers;
  the separation is effectively gone.
- Mounting Docker's own socket (`/var/run/docker.sock`) into a container:
  the container becomes able to run any container on the computer.
- `--network host` (unless needed): the network separation goes.

That is why Odyssey refuses `privileged`, `network_mode: host` and mounts
outside the working folder in compose exercises.

## What is inside the image

- **No secrets** (the Environment Variables section): no passwords via
  `ENV` / `ARG`; `.env` in `.dockerignore`.
- **No unneeded programs** (the Smaller Images section): build tools in a
  separate stage; every extra program is a possible hole.
- **A known base**: an official or verified publisher's image, with its
  version pinned.

## Staying up to date

Holes in base images are found and closed over time; fixes arrive with new
images. Pinning the version like `3.13-slim` lets the fixes arrive; but **your
image only gets them when it is rebuilt**:

```text
docker build --pull -t app .
```

`--pull` downloads the newest base image and builds with it. **Docker Scout**
in Docker Desktop can list the known holes in an image (Images › image ›
Vulnerabilities).

## Checklist

1. A pinned, trusted base image (`python:3.13-slim`).
2. `.dockerignore` (`.env`, `.git`); no secrets in the image.
3. Packages before `USER`; then `USER app`.
4. Folders written to are given to the user with `chown`.
5. A multi-stage build; only what is needed in the final image.
6. When running: no `--privileged`, no socket; `--read-only` and a memory
   limit if needed.
7. Regular `docker build --pull`.

## Summary

- A container is root by default; switch to a user with `RUN useradd ...` +
  `USER app`.
- After `USER`, folders created by root cannot be written to:
  `chown app:app` or `COPY --chown`.
- Reduce privileges when running: `--read-only`, `--cap-drop ALL`, a memory
  limit; no `--privileged` and no mounting the Docker socket.
- No secrets and no unneeded programs in the image; keep the base image
  current with `--pull`.
