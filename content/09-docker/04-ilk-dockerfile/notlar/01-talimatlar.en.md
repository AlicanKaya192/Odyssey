All the instructions you can use in a Dockerfile. You will see most of them
in detail in later sections of the path; the right column says where.

## Core instructions

| Instruction | What does it do? | Example | Section |
|---|---|---|---|
| `FROM` | Chooses the base image. Every Dockerfile starts with it. | `FROM python:3.13-slim` | 04 |
| `WORKDIR` | Sets the working folder (creates it if missing). | `WORKDIR /app` | 04 |
| `COPY` | Copies files from the context into the image. | `COPY . .` | 04 |
| `RUN` | Runs a command during the build; the result is a new layer. | `RUN pip install -r requirements.txt` | 04 |
| `CMD` | The default command when the container runs. | `CMD ["python", "app.py"]` | 04, 06 |
| `ENTRYPOINT` | The container's fixed entry command. | `ENTRYPOINT ["python", "cli.py"]` | 06 |

## Setting instructions

| Instruction | What does it do? | Example | Section |
|---|---|---|---|
| `ENV` | Defines an environment variable (valid while running too). | `ENV APP_ENV=production` | 08 |
| `ARG` | A variable valid only during the build. | `ARG VERSION=1.0` | 08 |
| `EXPOSE` | Documents the port the program listens on. | `EXPOSE 8000` | 07 |
| `USER` | Which user runs the following commands. | `USER app` | 13 |
| `VOLUME` | Marks the folder where data will be kept. | `VOLUME /data` | 09 |
| `LABEL` | Adds an information label to the image (author, version). | `LABEL version="1.0"` | — |
| `HEALTHCHECK` | A command that checks whether the container is healthy. | `HEALTHCHECK CMD curl -f http://localhost/` | 11 |

## Rarely used

| Instruction | What does it do? |
|---|---|
| `ADD` | Like `COPY`, but it can unpack compressed files and download from an address. Prefer `COPY` unless needed. |
| `SHELL` | Changes which shell `RUN` uses. |
| `STOPSIGNAL` | Changes the signal `docker stop` sends. |
| `ONBUILD` | An instruction that runs when another image is built from this one. |

## Common mistakes

- **`FROM` is not on the first line.** A Dockerfile must start with `FROM`
  (apart from comments and `ARG`).
- **A typo:** `FORM`, `COPPY`, `WORKIDR`. Docker says "unknown instruction";
  Odyssey tells you which line.
- **Running the program with `RUN`.** The program runs once while the image
  is built; what runs when the container starts is `CMD`.
- **More than one `CMD`.** Only the last one counts; the earlier ones are
  silently ignored.
