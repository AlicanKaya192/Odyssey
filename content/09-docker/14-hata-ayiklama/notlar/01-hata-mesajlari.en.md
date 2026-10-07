The most common Docker and Python error messages, their causes and fixes.
Search this page for part of the message.

## Build

| Message | Cause | Fix |
|---|---|---|
| `unknown instruction: FORM` | A typo in an instruction | Write the suggested name (`FROM`) |
| `"/x": not found` | The file is not in the context, or it is in `.dockerignore` | Check the name, folder, `.dockerignore` |
| `did not complete successfully: exit code: 1` | A `RUN` failed | The command's own error in the lines above |
| `No matching distribution found` | pip could not find the package (name, version or internet) | Check the package name and version |
| `pull access denied` / `not found` (in FROM) | The base image's name or tag is wrong | A correct name such as `python:3.13-slim` |
| `failed to connect to the docker API` | Docker Desktop is closed | Open Docker Desktop |

## Run

| Message | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'x'` | The file was not copied or the package not installed | `COPY`, requirements.txt |
| `can't open file '/app/app.py'` | The file is in another folder | `WORKDIR` and the `COPY` destination |
| `exec: "x": executable file not found in $PATH` | The command does not exist or is misspelt | `CMD` / `ENTRYPOINT` |
| `Permission denied` | The user cannot write to that folder | `chown` |
| `Address already in use` | The program tries to open the same port twice | A single server; the port setting |
| `port is already allocated` | The host port is taken | Another `-p` |
| `Connection refused` | The target is not listening (localhost, a stopped service) | Address, `0.0.0.0`, service name |
| `No address associated with hostname` | The service name is wrong or not on the same network | Name, network |
| `Read-only file system` | Writing is attempted with `--read-only` | A volume for the place written to |
| `Killed` / exit code 137 | The memory limit or a forced stop | `--memory`, `docker stats` |

## Compose

| Message | Cause | Fix |
|---|---|---|
| `did not find expected key` | The YAML indentation is broken | Spaces instead of tabs, alignment |
| `refers to undefined volume` | The named volume is not in `volumes:` at the bottom | Define it |
| `has no healthcheck configured` | No check on the service waited for with `service_healthy` | Add a `healthcheck` |
| `dependency failed to start` | The depended-on service could not start or is unhealthy | That service's log |
