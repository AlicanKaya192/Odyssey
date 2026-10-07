The most common surprising situations when using volumes and bind mounts.

## A mounted folder hides what was there

If the image has files in `/app` and you mount a folder from your computer
there with `-v ${PWD}:/app`, the container now sees **only the folder you
mounted**; the image's contents of `/app` are covered (not deleted, just not
visible).

This is a common cause of "my file was in the image but not in the
container".

When an **empty volume** is first mounted onto a folder, however, Docker
**copies** the image's files in that folder into the volume. If the volume is
not empty, it does not copy.

## How is the folder path written in which terminal?

| Terminal | The current folder |
|---|---|
| PowerShell | `-v ${PWD}:/app` |
| Command Prompt (cmd) | `-v %cd%:/app` |
| Git Bash | `-v "$(pwd)":/app` (path conversion can cause trouble) |
| Linux / Mac | `-v "$(pwd)":/app` |

A full path can be written too: `-v C:\Users\ada\project:/app`. If the path
has spaces, put it in quotes.

## `-v` or `--mount`?

Both do the same job. `--mount` is longer but clearer:

```text
--mount type=volume,source=notes,target=/data
--mount type=bind,source=${PWD},target=/app,readonly
```

With `-v`, if you misspell a path on your computer (the path does not exist),
Docker silently **creates an empty folder**; `--mount` fails instead.

## Permissions

If the program in the container runs as a non-root user (the Security
section), it may not be able to write to a mounted folder:
`PermissionError: [Errno 13] Permission denied: '/data/notes.txt'`. The fix
is to set the folder's owner in the Dockerfile (`chown`); in the Security
section.

## Speed on Windows

With a bind mount, files go back and forth between Windows and the Linux in
WSL 2; with many small files (e.g. `node_modules`, large data) it can slow
down. A volume lives inside Linux, so it is fast. Large data goes into a
volume.

## Which volumes are in use?

```text
docker ps --format "{{.Names}}: {{.Mounts}}"
docker volume ls --filter dangling=true    # those mounted on no container
```
