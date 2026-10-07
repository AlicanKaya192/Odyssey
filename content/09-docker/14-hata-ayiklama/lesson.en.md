# Debugging

When working with Docker there are two kinds of error: **the image cannot be
built**, or **the image builds but the container does not work**. The clues
for each sit in different places. This section explains, in order, where to
look for the problem and which tool to use.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>The image cannot be built</h4><p>The last lines of the <code>docker build</code> output</p><p>The failing step: <code>[3/5] RUN ...</code></p><p><code>--progress=plain --no-cache</code></p></div>
    <div class="dim"><h4>The container does not work</h4><p><code>docker ps -a</code> → exit code</p><p><code>docker logs</code> → last words</p><p><code>--entrypoint sh</code> → look inside</p></div>
  </div>
  <figcaption>First decide which phase the error is in; the clues are in different places.</figcaption>
</figure>

## 1. Build errors

When a build fails, Docker writes in the last lines **which step** failed.
Look at that first.

**A typo:**

```text
ERROR: failed to build: failed to solve: dockerfile parse error on line 1:
unknown instruction: FORM (did you mean FROM?)
```

The line number and a suggestion come together.

**A file not in the context:**

```text
failed to calculate checksum of ref ...: "/app.pyy": not found
```

The file's name is wrong, or `.dockerignore` leaves it out.

**A `RUN` command failing:**

```text
ERROR: failed to build: failed to solve: process "/bin/sh -c false"
did not complete successfully: exit code: 1
```

The command that ran is in quotes. The real cause is usually **above** this
line: the error the command itself printed (pip's "No matching
distribution", a Python error...). To see the whole output:

```text
docker build --progress=plain --no-cache -t app .
```

`--progress=plain` prints the whole output of each step as plain text,
`--no-cache` really runs the step instead of taking it from the cache.

## 2. Run errors

The image was built and the container starts but ends at once or behaves
wrongly.

**Step 1: the container's state.**

```text
docker ps -a
```

`Exited (1) Less than a second ago` → the program ended with an error. By
exit code (the note in the First Containers section): 1 a program error, 125
Docker could not start it, 127 command not found, 137 killed.

**Step 2: the program's last words.**

```text
docker logs web
```

```text
Traceback (most recent call last):
  File "/app/main.py", line 1, in <module>
    from helpers import greet
ModuleNotFoundError: No module named 'helpers'
```

Python's error output is the same here too. `helpers.py` is not in the image:
the Dockerfile copied only `main.py`.

**Step 3: look inside the image.** The container ends too quickly to get in
with `exec`. Open a **new** container from the same image with a different
command:

```text
docker run --rm -it --entrypoint sh app
# ls -la /app
```

or with a single command:

```text
docker run --rm --entrypoint ls app -la /app
-rwxr-xr-x 1 root root   41 Oct  6 20:26 main.py
```

Only `main.py` is there; the guess is confirmed.

## 3. More tools

| Command | What does it show? |
|---|---|
| `docker inspect web` | All the container's settings (command, environment, mounts, exit code) |
| `docker logs --tail 50 -f web` | The last 50 lines and then live |
| `docker exec -it web sh` | A shell inside the running container |
| `docker cp web:/app ./copied` | Copies files from the container to the computer (even if stopped) |
| `docker diff web` | Files the container added (A) and changed (C) compared with the image |
| `docker image inspect app` | The image's settings (CMD, ENV, WORKDIR, USER) |

## 4. Common situations

| Symptom | Most likely | Look at |
|---|---|---|
| `No module named 'x'` | The file was not copied or the package not installed | `ls /app`, requirements.txt |
| `can't open file '/app/app.py'` | The file was copied to another folder; WORKDIR and COPY disagree | Where the file is, with `ls` |
| `exec: "pyhton": executable file not found` (127) | A typo in the command | The `CMD` line |
| The container is `Exited (0)` at once | The program finished its job (not a server) or CMD is wrong | `docker inspect` → Cmd |
| `Permission denied` | Writing to root's folder after `USER` | `chown` (Security) |
| The page does not open | The port, 0.0.0.0, or the program crashed | The Ports section's note |
| My change does not show | The old image is running; it was not rebuilt | `docker build`, `up --build` |

## 5. The method

1. **Which phase?** Build or run?
2. **Read the last lines.** The error is almost always in the last ten
   lines.
3. **Guess, then confirm.** If it says "no file", look inside (`ls`); if it
   says "port", `docker port`.
4. **Change one thing and try again.** If you change three things at once,
   you cannot know which one fixed it.

## Summary

- For a build error, look at the failing step and the lines above it;
  `--progress=plain --no-cache` shows the whole output.
- For a run error, the order: `docker ps -a` (exit code) → `docker logs` →
  look inside the image with `--entrypoint sh`.
- `inspect`, `exec`, `cp`, `diff` for examining a container.
- Guess, change one thing, confirm.
