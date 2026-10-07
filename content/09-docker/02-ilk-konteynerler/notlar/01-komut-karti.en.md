All of this section's commands on one page. You do not need to memorise
them; your fingers will learn them over time.

## Running: `docker run`

```text
docker run [options] image [command]
```

| Option | Long name | What does it do? |
|---|---|---|
| `--name web` | | Names the container. |
| `--rm` | | Removes the container automatically when it ends. |
| `-d` | `--detach` | Runs it in the background and gives the terminal back. |
| `-i` | `--interactive` | Passes what you type to the container. |
| `-t` | `--tty` | Gives the container a terminal. |
| `-it` | | `-i` and `-t` together: to go inside. |

Short options can be combined: `-dit` instead of `-d -i -t`. Options are
written **before the image name**; everything after the image counts as the
container's command.

```text
docker run --rm alpine:3.22 echo hi        # right: --rm is Docker's option
docker run alpine:3.22 --rm echo hi        # wrong: --rm goes to the container as a command
```

## Listing

| Command | What does it show? |
|---|---|
| `docker ps` | Running containers |
| `docker ps -a` | All of them, finished ones included |
| `docker ps -q` | Only the identities (to hand to other commands) |

## With a running container

| Command | What does it do? |
|---|---|
| `docker logs name` | The container's output so far |
| `docker logs -f name` | Follows the output live (leave with Ctrl+C) |
| `docker logs --tail 20 name` | Only the last 20 lines |
| `docker exec name command` | Runs a command in the running container |
| `docker exec -it name sh` | Goes inside the running container with a shell |

## Stopping and removing

| Command | What does it do? |
|---|---|
| `docker stop name` | Stops it (gives the program time to shut down) |
| `docker start name` | Starts a stopped container again |
| `docker restart name` | Stops and starts it again |
| `docker rm name` | Removes a stopped container |
| `docker rm -f name` | Removes it by force even if it is running |
| `docker container prune` | Removes all stopped containers (asks for confirmation) |

## Ways to refer to a container

You can refer to a container in three ways:

- by its name: `docker stop sleeper`,
- by its full identity,
- by the start of its identity: `docker stop 3b8f` (as long as no other
  identity starts with the same characters).

## `run`, `start` or `exec`?

- `run` → creates a **new** container and runs it.
- `start` → runs an **existing, stopped** container again.
- `exec` → runs an extra command inside an **existing, running** container.
