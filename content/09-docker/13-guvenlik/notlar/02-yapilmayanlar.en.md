Things that look like shortcuts but remove security. If you see them in
instructions or on the internet, think twice.

| Done | Why is it dangerous? | Instead |
|---|---|---|
| `docker run --privileged` | The container gets almost all of the computer's powers. | Give the one power needed with `--cap-add`. |
| `-v /var/run/docker.sock:/var/run/docker.sock` | The container can manage Docker: it can start any container with any power. | Do not, unless really needed. |
| `-v /:/host` | The computer's whole disk is in the container. | Mount only the folder needed, `:ro` if possible. |
| `ENV PASSWORD=...` | The password shows in `docker image inspect`. | `--env-file` when running. |
| `FROM someone/random-image` | Nobody knows what is inside. | An official or verified image. |
| `FROM python` | `latest`; what gets installed is unclear. | `FROM python:3.13-slim`. |
| `chmod -R 777 /app` | Everyone can write everything. | `chown app:app` only on the folder written to. |
| `curl ... \| sh` (in a Dockerfile) | Running a downloaded script without looking. | A package with a pinned version and a checked digest. |
| `-p 0.0.0.0:5432:5432` (a database) | The database is open to everyone on the network. | Do not publish the port; let it be reached from the same network. |

## Ask yourself

- If this container were taken over, what would the attacker reach?
- Would the program work without this file in the image? (If so, take it
  out.)
- Must this port really be open to the outside?
- When was this image last rebuilt?
