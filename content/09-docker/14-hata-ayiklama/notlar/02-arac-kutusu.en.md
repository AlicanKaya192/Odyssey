The most useful commands when debugging, with when to use them.

## The container does not start or ends at once

```text
docker ps -a                             # state and exit code
docker logs web                          # what it printed last
docker run --rm -it --entrypoint sh app  # look inside the same image
```

## The container runs but behaves wrongly

```text
docker logs -f --tail 50 web             # live log
docker exec -it web sh                   # walk around inside
docker exec web env                      # are the environment variables right?
docker top web                           # which processes are inside?
docker stats                             # memory and processor use (live)
```

## Are the settings right?

```text
docker inspect web --format "{{.Config.Cmd}}"          # command
docker inspect web --format "{{.Config.Env}}"          # environment
docker inspect web --format "{{json .Mounts}}"         # mounts
docker inspect web --format "{{.State.ExitCode}}"      # exit code
docker port web                                         # ports
```

## Files

```text
docker cp web:/app/output.txt .          # container to computer
docker cp ./config.json web:/app/        # computer to container
docker diff web                          # what changed compared with the image
```

`docker cp` works on a stopped container too: handy for taking the log file a
crashed program left behind.

## Build

```text
docker build --progress=plain --no-cache -t app .   # the whole output
docker build --target build -t app:debug .          # stop at a stage
docker history app                                  # which layer is what
```

## In Odyssey

Odyssey's terminal shows the build steps (`CACHED` / `DONE`), the last lines
of a build error and the container's output. If you need more detail, build
the same Dockerfile yourself in PowerShell and examine it with these
commands.
