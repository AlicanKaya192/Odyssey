# CMD, ENTRYPOINT and Arguments

So far you have told the container what to run with `CMD`. In this section
we will look at every detail of the command that runs when a container
starts: changing `CMD` from outside, the difference between the two ways of
writing it, turning a container into a command-line tool with `ENTRYPOINT`,
and how `docker stop` shuts the program down.

## `CMD` is only the default

`CMD` is the container's **default** command: the one that runs if
`docker run` is given no command. If a command is given, the **whole** of
`CMD` is replaced by it:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

```text
docker run --rm greeter                                  # python app.py
docker run --rm greeter python -c "print('other work')"  # CMD ignored
```

In the second line `app.py` never ran: everything you wrote after the image
name took the place of `CMD`.

## Two forms: exec and shell

`CMD` can be written in two forms:

```dockerfile
CMD ["python", "app.py"]     # exec form (square brackets, JSON)
CMD python app.py            # shell form
```

The difference is bigger than it looks. In the shell form Docker hands the
command to a shell itself; what is actually written into the image is this:

```text
docker image inspect demo --format "{{.Config.Cmd}}"
[/bin/sh -c python app.py]
```

So the container's main program (process number 1) is **`sh`, not Python**;
Python runs under it. This has two consequences:

**1. Variables.** The shell expands variables such as `$NAME`; the exec form
does not.

```dockerfile
ENV NAME=Ada
CMD echo hi $NAME            # output: hi Ada
CMD ["echo", "hi $NAME"]     # output: hi $NAME  (as it is)
```

If you need a variable in the exec form, call the shell explicitly:
`CMD ["sh", "-c", "echo hi $NAME"]`.

**2. The shutdown signal.** In the next heading.

The rule: **use the exec form by default.** Use the shell form only when you
really need a shell feature (variables, `&&`, `|`), and then as
`["sh", "-c", "..."]`.

## How does `docker stop` shut down?

`docker stop` sends **SIGTERM** to the container's process number 1: "you are
asked to shut down, tidy up your work". It waits a while; if the program does
not close, it kills it by force with **SIGKILL** (exit code 137).

We tried three times with the same program; the program was sleeping for 600
seconds and `docker stop` was called:

| How it ran | `docker stop` time | Exit code |
|---|---|---|
| `CMD ["python", "app.py"]` | 3.8 s | 137 (killed by force) |
| `CMD python app.py` (shell) | 3.7 s | 137 (killed by force) |
| Python catching SIGTERM | 0.6 s | 0 (closed properly) |

- **In the shell form** the signal goes to `sh` and never reaches Python.
- **In the exec form** the signal reaches Python, but if a program running as
  process number 1 does not **catch** the signal itself, Linux ignores it.
  The fix: the program should listen for the signal.

```python
import signal
import sys

def stop(signum, frame):
    print("shutting down, saving the work", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, stop)
```

Or, without touching the code, have Docker add a small starter:
`docker run --init ...` passes the signals on to the program (the program
closes with code 143). Web frameworks (such as uvicorn, which runs FastAPI)
already catch SIGTERM.

Why does it matter? A program killed by force can leave a half-written file
or fail to finish a record it was writing to a database.

## `ENTRYPOINT`: the fixed command

`ENTRYPOINT` is the command the container **always** runs. What you give to
`docker run` does not replace it; it is **appended to it as arguments**. In
this case `CMD` becomes the default arguments:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY greet.py .
ENTRYPOINT ["python", "greet.py"]
CMD ["World"]
```

```text
docker run --rm greet                 # python greet.py World
docker run --rm greet Ada Lovelace    # python greet.py Ada Lovelace
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">ENTRYPOINT<br><small>python greet.py</small></span><span class="arrow">+</span>
    <span class="node">CMD (default)<br><small>World</small></span><span class="arrow">or</span>
    <span class="node ok">what is written to docker run<br><small>Ada Lovelace</small></span>
  </div>
  <figcaption><code>ENTRYPOINT</code> always runs; either <code>CMD</code> or what is written after the image in <code>docker run</code> is appended to it.</figcaption>
</figure>

`greet.py` reads the arguments from Python's `sys.argv` list; `sys.argv[1:]`
is what was written after the image name (or `CMD`).

```python
import sys

names = sys.argv[1:]
print("Hello,", " ".join(names) + "!")
```

This way the image is used like a **command-line tool**:
`docker run --rm greet Ada`.

If you need to change `ENTRYPOINT` once (e.g. to look inside):

```text
docker run --rm -it --entrypoint sh greet
```

## Which when?

| Situation | Write |
|---|---|
| An application; someone may want to run something else | Only `CMD ["python", "app.py"]` |
| The image is a single tool that takes arguments | `ENTRYPOINT ["python", "tool.py"]` + a default `CMD ["--help"]` |
| A variable or `&&` is needed | `CMD ["sh", "-c", "..."]` |

If `ENTRYPOINT` and `CMD` are written together, **both must be in the exec
form**. A shell-form `ENTRYPOINT` ignores `CMD`.

## Summary

- `CMD` is the default command; `docker run image command` replaces it
  entirely.
- The exec form (`["python", "app.py"]`) runs the program directly, the shell
  form through `/bin/sh -c`. The shell form expands variables but does not
  pass the signal to the program. **Default: exec.**
- `docker stop` sends SIGTERM first, then SIGKILL (137). The program should
  catch SIGTERM, or `--init` should be used.
- `ENTRYPOINT` is the fixed command; what is written to `docker run` and
  `CMD` become its arguments. `--entrypoint` changes it once.
- Python reads the arguments from `sys.argv[1:]`.
