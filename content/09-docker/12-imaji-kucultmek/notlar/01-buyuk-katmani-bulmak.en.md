Ways to find out why an image is big.

## `docker history`

```text
docker history app --format "{{.Size}}\t{{.CreatedBy}}"
```

Each layer's size and the instruction that created it. Look at the biggest
numbers:

| If you see | Most likely |
|---|---|
| `COPY . .` hundreds of MB | `.dockerignore` missing (`.git`, `.venv`, data) |
| `RUN pip install` very big | No `--no-cache-dir`, or unneeded packages |
| The delete line 0 B but the one before big | The delete is in a separate `RUN`; move it to the same line |
| `apt-get install` big | No `--no-install-recommends`, list not cleaned |

## Looking inside the image

```text
docker run --rm app du -sh /app /usr/local/lib/python3.13/site-packages
```

`du -sh` prints the space a folder takes. An unexpectedly big folder is
usually something copied by mistake.

## Seeing the size as a number

```text
docker image inspect app --format "{{.Size}}"
```

In bytes. Odyssey's `max_size_mb` check looks at this number.

## Shared layers

The sizes in `docker images` do not count layers as shared: five images built
from the same `python:3.13-slim` each appear above 180 MB, but on disk the
Python layers sit once. For real usage, `docker system df`.

## A more visual tool

The open-source tool `dive` opens an image layer by layer and shows which
files were added in each layer. We do not install it in this path, but it is
useful in large projects.
