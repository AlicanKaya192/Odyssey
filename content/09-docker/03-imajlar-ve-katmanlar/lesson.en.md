# Images, Tags and Layers

So far you have used the `alpine:3.22` and `python:3.13-slim` images. In this
section we will look closely at the image itself: how its name is read, how
its version is told, why it is made of stacked slices and how it is managed
on the computer.

## Reading an image's name

`python:3.13-slim` is actually a shortened name. Its full form is:

<figure class="fig">
  <div class="anat">
    <div class="sig"><code>docker.io / library / python : 3.13-slim</code></div>
    <div class="anat-row"><span>docker.io</span><span><b>Registry</b>: where the image is downloaded from (Docker Hub). The default.</span></div>
    <div class="anat-row"><span>library</span><span><b>Namespace</b>: the publisher. <code>library</code> for official images; the default.</span></div>
    <div class="anat-row"><span>python</span><span><b>Repository</b>: the image's name.</span></div>
    <div class="anat-row"><span>3.13-slim</span><span><b>Tag</b>: version and variant. <code>latest</code> if omitted.</span></div>
  </div>
  <figcaption>When you write <code>python:3.13-slim</code>, Docker adds the first two parts itself.</figcaption>
</figure>

- **Registry**: where the image is downloaded from. If omitted, Docker Hub
  (`docker.io`).
- **Namespace**: who publishes the image. For Docker's official images it is
  `library`, assumed when omitted. A person's image looks like `ada/myapp`.
- **Repository**: the image's name, `python`.
- **Tag**: what comes after `:`, usually a version. `3.13-slim`.

So when you type `docker pull python:3.13-slim`, Docker downloads
`docker.io/library/python:3.13-slim`. The last line of the `docker pull`
output prints this full name too.

## Tags: versions of the same image

A repository can have dozens of tags. A few from the `python` repository:

| Tag | What? | Approximate size |
|---|---|---|
| `3.13` | Python 3.13 on a full Debian (build tools included) | ~1 GB |
| `3.13-slim` | Python 3.13 on a trimmed Debian | ~180 MB |
| `3.13-alpine` | Python 3.13 on Alpine | ~50 MB |
| `3.13.16-slim` | Exactly 3.13.16 | ~180 MB |
| `latest` | Used when no tag is given | varies |

A tag carries two pieces of information: **the Python version** (`3.13`)
and **the Linux underneath** (`slim`, `alpine`; sometimes the name of the
Debian release: `trixie`, `bookworm`).

## `latest` does not mean newest

If you do not write a tag, Docker uses the `latest` tag:

```text
docker pull python          # = docker pull python:latest
```

`latest` is not a magic word; it is the tag the publisher chose as the
"default". Today it points to Python 3.13, tomorrow it may point to 3.14.
The same Dockerfile can work today and break a month later.

Hence the rule: **always write the image's version** ("pinning" it). Write
`FROM python:3.13-slim` instead of `FROM python:latest` or just
`FROM python`.

If you want to be even more exact, you can write the image's **digest**: an
identity computed from the image's contents that never changes.

```text
docker pull alpine:3.22
...
Digest: sha256:5291449c3df73caf6ed85e649dec1b9e818b39a5d8c871e97afc13e9cd5e8fa8
```

With `FROM alpine@sha256:5291449c...` exactly that image is downloaded every
time. A tag can be moved like a bookmark; a digest cannot.

## Layers

An image is not a single file; it is made of **stacked slices** (layers).
Each slice holds what was added or changed compared with the one below.

`docker history` shows an image's layers:

```text
docker history alpine:3.22
```

```text
IMAGE          CREATED       CREATED BY                                      SIZE
5291449c3df7   2 weeks ago   CMD ["/bin/sh"]                                 0B
<missing>      2 weeks ago   ADD alpine-minirootfs-3.22.6-x86_64.tar.gz /…   8.97MB
```

Read it from the bottom up: first Alpine's files were added (8.97 MB), then
the default command was set to `/bin/sh` (0 B; only a setting, no files
added).

`python:3.13-slim` is a little more crowded:

```text
CREATED BY                                   SIZE
CMD ["python3"]                              0B
RUN /bin/sh -c set -eux; for src in idle3…   16.4kB
RUN /bin/sh -c set -eux; savedAptMark=…      40.4MB
ENV PYTHON_VERSION=3.13.16                   0B
RUN /bin/sh -c set -eux; apt-get update; …   4.94MB
ENV PATH=/usr/local/bin:…                    0B
# debian.sh --arch 'amd64' out/ 'trixie' …   87.7MB
```

At the bottom are the files of Debian "trixie" (87.7 MB), above them a few
system packages, then Python itself (40.4 MB), and the default command at the
top. Instructions that add files (`RUN`, `COPY`, `ADD`) carry size; setting
instructions (`ENV`, `CMD`) are 0 B.

<figure class="fig">
<svg viewBox="0 0 620 212" width="620" xmlns="http://www.w3.org/2000/svg">
  <rect class="box" x="30" y="4" width="380" height="30" rx="6" stroke-dasharray="5 4"/>
  <text class="ink" x="44" y="24" font-size="13">The container's writable layer</text>
  <rect class="box" x="30" y="40" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="63" font-size="13">CMD ["python3"]</text>
  <text class="dim" x="396" y="63" font-size="12" text-anchor="end">0 B</text>
  <rect class="box" x="30" y="82" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="105" font-size="13">Python 3.13.16</text>
  <text class="dim" x="396" y="105" font-size="12" text-anchor="end">40.4 MB</text>
  <rect class="box" x="30" y="124" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="147" font-size="13">System packages</text>
  <text class="dim" x="396" y="147" font-size="12" text-anchor="end">4.9 MB</text>
  <rect class="box" x="30" y="166" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="189" font-size="13">Debian trixie files</text>
  <text class="dim" x="396" y="189" font-size="12" text-anchor="end">87.7 MB</text>
  <line class="line" x1="428" y1="40" x2="428" y2="202"/>
  <line class="line" x1="420" y1="40" x2="428" y2="40"/>
  <line class="line" x1="420" y1="202" x2="428" y2="202"/>
  <text class="ink" x="440" y="118" font-size="13" font-weight="600">python:3.13-slim</text>
  <text class="dim" x="440" y="136" font-size="12">read-only, shared</text>
  <text class="dim" x="440" y="24" font-size="12">← gone when the container is removed</text>
</svg>
  <figcaption>An image is layers stacked from the bottom up. A container adds its own thin layer on top; it never touches the image's layers.</figcaption>
</figure>

## Why do layers matter?

**1. They are shared.** If two images have the same lower layers, those
layers sit on disk **once**. If you build ten images starting from Python,
Python's layers take up space once, not ten times; only the top layers you
add are separate.

**2. They are downloaded once.** `docker pull` downloads only the layers that
are not on your computer. When a new version comes out, often only a few top
layers are downloaded.

**3. The build cache is built on them.** When you build your own image,
unchanged layers are not created again; the build drops to seconds. We will
see this in detail in the Cache section.

**4. The container's writable layer.** An image's layers are read-only. When
a container runs, a **thin, writable layer** is added on top; every change
you make inside the container goes there. When the container is removed,
that layer goes too; that is why the file disappeared in the previous
section.

## Inspecting an image

`docker image inspect` gives all of an image's settings as JSON. It is a
long output; you can pick a particular field with `--format`:

```text
docker image inspect python:3.13-slim --format "{{.Config.Cmd}}"
```

```text
[python3]
```

If you run a container from this image without a command, `python3` opens.
Other useful fields: `{{.Config.Env}}` (environment variables),
`{{.Os}}/{{.Architecture}}` (which system it is for: `linux/amd64`).

## Giving your own name: `docker tag`

`docker tag` gives an existing image **a second name**. The image is not
copied; a new tag is stuck onto the same image:

```text
docker tag alpine:3.22 mybase:1.0
docker images
```

```text
IMAGE              ID             DISK USAGE   CONTENT SIZE
alpine:3.22        5291449c3df7       12.8MB         3.88MB
mybase:1.0         5291449c3df7       12.8MB         3.88MB
```

The **ID of the two rows is the same**: one image, two names. When you
publish your own images you can give tags such as `myapp:1.0` and
`myapp:1.1` and still reach the old ones.

## Removing and cleaning up

```text
docker rmi mybase:1.0           # remove a name (a tag)
docker image rm alpine:3.22     # the same, in its long form
docker image prune              # remove nameless (dangling) images
docker system prune             # stopped containers, nameless images, idle networks, cache
```

- If an image has several names, `docker rmi` removes only that name
  (`Untagged: mybase:1.0`); the image goes when its last name is removed.
- If a container (even a stopped one) uses an image, the image cannot be
  removed; remove the container first.
- **Nameless image** (dangling): when you build a new image with the same
  name, the old one loses its name and stays as `<none>`. `docker image
  prune` cleans these up.
- `prune` commands tell you what they will remove and ask for confirmation.

## Choosing images on Docker Hub

Anyone can publish images on Docker Hub. Signs to look for before trusting
one:

- **Docker Official Image**: images maintained by Docker together with the
  software's owners (`python`, `alpine`, `postgres`, `nginx`). There is no
  namespace in their name.
- **Verified Publisher**: images of companies whose identity has been
  verified.
- Stay away from images that have not been updated for a long time and whose
  publisher is unknown: you do not know what is inside.

## Summary

- Full name: `registry/namespace/repository:tag`; `python:3.13-slim` =
  `docker.io/library/python:3.13-slim`.
- A tag tells the version and the Linux underneath. `latest` does not mean
  newest; **always pin the version**. The most exact is the digest
  (`@sha256:...`).
- An image is made of stacked **layers** (`docker history`); layers are
  shared, downloaded once and the basis of the build cache.
- A container adds its own writable layer on top.
- `docker image inspect` for settings, `docker tag` for a new name,
  `docker rmi` for removing, `docker image prune` for cleaning up nameless
  ones.
