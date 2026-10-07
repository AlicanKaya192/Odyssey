# Keeping Data: Volumes and Bind Mounts

In the First Containers section we set a rule: do not write anything
important inside a container; it goes when the container is removed. So what
about a database, a notes app, uploaded files? Data must stay somewhere. In
Docker that place comes in two forms: **volumes** and **bind mounts**.

## The problem: the writable layer is temporary

Everything you write inside a container goes to its thin, writable layer.
When the container is removed, the layer goes too. When you release a new
version, you remove the old container and run the new one; if the data is
inside the container, it is lost on every update.

The fix: keep the data **outside** the container and **mount** it onto a
folder inside the container.

<figure class="fig">
  <div class="flow">
    <span class="node">Container 1<br><small>writes /data/n.txt</small></span><span class="arrow">→</span>
    <span class="node acc">Volume: notes<br><small>outside the container</small></span><span class="arrow">→</span>
    <span class="node ok">Container 2<br><small>reads /data/n.txt</small></span>
  </div>
  <figcaption>Both containers were removed; the data stayed in the volume. The container's <code>/data</code> folder is actually the volume itself.</figcaption>
</figure>

## Volume: a store managed by Docker

A **volume** is a named data area that Docker creates and manages for you.
Create one and mount it onto a container:

```text
docker volume create notes
docker run --rm -v notes:/data alpine:3.22 sh -c "echo first > /data/n.txt"
docker run --rm -v notes:/data alpine:3.22 cat /data/n.txt
```

```text
first
```

Two **separate** containers; both ran with `--rm` and were removed. But the
second read the file the first wrote, because the file is not in a container
but in the `notes` volume.

`-v notes:/data` says: **mount the `notes` volume onto the container's
`/data` folder.** The program in the container thinks it is writing to an
ordinary folder.

If the volume does not exist, `-v` creates it by itself; writing
`volume create` is not required, but it shows clearly what you are doing.

## Volume commands

```text
docker volume ls                  # all volumes
docker volume inspect notes       # details
docker volume rm notes            # remove (if no container uses it)
docker volume prune               # volumes no container uses
```

```text
docker volume ls
DRIVER    VOLUME NAME
local     notes
```

`docker volume inspect` tells where the volume lives:
`/var/lib/docker/volumes/notes/_data`. This path is inside Docker's Linux
(WSL 2); it is not directly visible in Windows' file explorer. You reach a
volume through containers.

**Careful:** `docker volume rm` and `docker volume prune` delete the data
**for good**. Removing a container does not touch the volume; removing the
volume takes the data with it.

## `VOLUME` in the Dockerfile

```dockerfile
VOLUME /data
```

It **documents** for whoever uses the image: "this program's data is in
`/data`; mount a volume there". If `-v` is not given, Docker creates a
nameless volume for that folder; the data does not stay in the container's
writable layer, but since the name is random it is hard to find. Giving your
own named volume with `-v` is always better.

## Bind mount: a folder on your computer

A **bind mount** mounts **a particular folder on your computer** into the
container. The container sees that very folder; a change made on one side
appears on the other at once.

Mounting the current folder in PowerShell:

```text
docker run --rm -v ${PWD}:/app -w /app python:3.13-slim python app.py
```

- `${PWD}`: "the current folder" in PowerShell.
- `-w /app`: the container's working folder (like `WORKDIR`).

Without building an image, this runs the `app.py` on your computer with the
Python 3.13 in the container. Edit the code and run the command again, and
the new version runs. Very handy **during development**.

If you want the container only to **read** a folder, add `:ro` (read-only)
at the end:

```text
docker run --rm -v ${PWD}/config:/config:ro app
```

## Which when?

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Volume</h4><pre><code class="language-text">-v notes:/data</code></pre><p>Managed by Docker</p><p>Databases, uploaded files</p></div>
    <div><h4>Bind mount</h4><pre><code class="language-text">-v ${PWD}:/app</code></pre><p>A folder on your computer</p><p>Code during development, settings</p></div>
  </div>
  <figcaption>If there is a name to the left of the colon it is a volume; if there is a path, a bind mount.</figcaption>
</figure>

| | Volume | Bind mount |
|---|---|---|
| Written as | `-v notes:/data` (a name) | `-v ${PWD}:/app` (a path) |
| Where does it live? | Inside Docker | In a folder on your computer |
| Who manages it? | Docker | You |
| Typical use | Database data, uploaded files | Code during development, a settings file |
| Moving to another computer | With commands (by backing up) | The folder is already yours |

The rule: **the data itself in a volume, the code you develop in a bind
mount.** A released image is not given its code with a bind mount; the code
must be inside the image (`COPY`).

## Backing up a volume

A small container is used to put a volume's contents into a file: it mounts
both the volume and a folder on your computer and archives with `tar`.

```text
docker run --rm -v notes:/data -v ${PWD}:/backup alpine:3.22 `
  tar czf /backup/notes.tgz -C /data .
```

The `` ` `` at the end of the line means "the command continues on the next line" in PowerShell (`\` in bash). This single command has both kinds of mount from this section together.

## Summary

- A container's writable layer is temporary; lasting data is kept outside
  and **mounted** into the container.
- **Volume:** `-v name:/folder`; managed by Docker, it stays even when the
  container is removed. `docker volume ls / inspect / rm / prune`. `rm` and
  `prune` delete the data.
- `VOLUME /data` documents where the data lives; giving a name with `-v` is
  better.
- **Bind mount:** `-v ${PWD}:/app`; the very folder on your computer. For
  code during development; `:ro` for read-only.
- Data in a volume, code under development in a bind mount, released code
  inside the image.
