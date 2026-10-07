The multi-stage build is not only for shrinking; it is also used for several
purposes in one Dockerfile.

## A test stage

```dockerfile
FROM python:3.13-slim AS base
WORKDIR /app
COPY . .

FROM base AS test
RUN python -m unittest

FROM base AS runtime
CMD ["python", "main.py"]
```

- `FROM base`: starting from another stage; the shared steps are written
  once.
- `docker build --target test .` runs the tests; if they fail, the build
  fails.
- `docker build .` builds the last stage (`runtime`); the tests do not go
  into the image.

## Development and production

```dockerfile
FROM python:3.13-slim AS runtime
...
CMD ["python", "main.py"]

FROM runtime AS dev
ENV DEBUG=true
CMD ["python", "main.py", "--reload"]
```

Choosing which one to build in Compose:

```yaml
services:
  web:
    build:
      context: .
      target: dev
```

## Taking a file from a ready-made image

`COPY --from` takes not only a stage name but also an image name:

```dockerfile
COPY --from=alpine:3.22 /bin/busybox /usr/local/bin/busybox
```

For taking a tool without carrying the whole image. Careful: the libraries
the copied file needs to run must also be in the new image.

## Stage order and the cache

Each stage has its own cache. A stage the last stage does not need is
**skipped** during `docker build` (BuildKit): the test stage does not run in
the default build; only with `--target test`.
