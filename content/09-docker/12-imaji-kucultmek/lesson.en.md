# Smaller Images: Multi-Stage Builds

The bigger an image, the slower it downloads, the more space it takes and the
more unneeded programs sit inside it (each a possible security hole). In this
section we will measure why an image grows and learn the strongest way to
shrink it: the **multi-stage build**.

## Where does the size come from?

`docker images` shows each image's size:

```text
IMAGE              DISK USAGE
python:3.13-slim        178MB
alpine:3.22            12.8MB
```

Your own image's size = the base image + the layers you add. `docker history`
tells how much each layer holds; if you see a big number, look there.

## Deleting does not shrink a layer

Let us create a file and delete it on the next line:

```dockerfile
FROM alpine:3.22
RUN head -c 30000000 /dev/urandom > /big.bin
RUN rm /big.bin
```

The file is not in the image, but:

```text
docker history odyssey-a
4.1kB   RUN /bin/sh -c rm /big.bin
30MB    RUN /bin/sh -c head -c 30000000 /dev/urandom…
```

The image is **72.8 MB**. Every `RUN` is a layer and layers sit on top of
each other: the second layer only **marks** the file as "deleted"; the 30 MB
in the first layer is still there. (The image size also counts the layers'
uncompressed form.)

The same work in **one** `RUN`:

```dockerfile
RUN head -c 30000000 /dev/urandom > /big.bin && rm /big.bin
```

The image is **12.8 MB**: the size of Alpine itself. The file was created and
deleted in the same layer, so it never entered the layer.

The rule: **delete a temporary file in the `RUN` that created it.** That is
why caches are cleaned on the same line when installing packages
(`pip install --no-cache-dir`, `apt-get ... && rm -rf /var/lib/apt/lists/*`).

## The multi-stage build

Often the tools needed to **produce** something are not needed to **run**
it: compilers, test tools, source files. A multi-stage build has **several
`FROM` lines** in one Dockerfile; each `FROM` starts a new stage, and only the
**last stage** goes into the final image.

An example: we produce an HTML report with Python, but carrying the report
does not need Python.

```dockerfile
FROM python:3.13-slim AS build
WORKDIR /src
COPY build_report.py .
RUN python build_report.py

FROM alpine:3.22
COPY --from=build /out /report
CMD ["cat", "/report/index.html"]
```

- `AS build`: names the stage.
- In the first stage Python produces the report and writes it to `/out`.
- The second `FROM` starts from scratch with a clean Alpine.
- `COPY --from=build /out /report`: take **only** the files needed from
  another stage.

<figure class="fig">
  <div class="flow">
    <span class="node">Stage 1: build<br><small>python:3.13-slim · 176 MB</small></span><span class="arrow">→ COPY --from=build /out →</span>
    <span class="node ok">Stage 2 (final image)<br><small>alpine:3.22 · 12.8 MB</small></span>
  </div>
  <figcaption>The first stage produces and is thrown away; only the last stage and the result copied there go into the final image.</figcaption>
</figure>

The result:

```text
IMAGE           DISK USAGE
report          12.8MB
report:build    176MB
```

The final image is 12.8 MB and has **no** Python inside: the production tools
stayed in the first stage.

## Building one stage on its own: `--target`

```text
docker build --target build -t report:build .
```

The build stops at the `build` stage; handy for inspecting the intermediate
result or running tests (that was the 176 MB image).

## In Python applications

A pure Python application stays on `python:3.13-slim` (it needs Python to
run); but a multi-stage build still helps:

```dockerfile
FROM python:3.13 AS build
WORKDIR /src
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.13-slim
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . /app
CMD ["python", "/app/main.py"]
```

Packages that need compiling (libraries with C extensions) are prepared in
the **large** image with its build tools; only the ready packages go into the
final image. (This example downloads packages from the internet, so it is not
run in this path.)

## A shrinking checklist

1. The right base: `-slim` (or `alpine` if suitable), not the full image.
2. `.dockerignore`: `.git`, `.venv`, data left out.
3. `pip install --no-cache-dir`; temporary files deleted in the same `RUN`.
4. Production tools in a separate stage; only the result in the last stage.
5. Find the biggest layer with `docker history`.

## Summary

- Image size = base + layers; `docker history` shows the big layer.
- Deleting in a later `RUN` does not shrink the image (72.8 MB); deleting in
  the same `RUN` does (12.8 MB).
- Multi-stage build: several `FROM` lines, `AS name`, `COPY --from=name`;
  only the last stage goes into the image (176 MB → 12.8 MB).
- `--target name` stops the build at that stage.
