A container can be stopped at any moment: you say `docker stop`, the server
restarts, a new version arrives. At that moment the program needs to finish
its work properly.

## The order of stopping

1. Docker sends **SIGTERM** to process number 1.
2. It waits (the default time; 30 seconds with `docker stop -t 30`).
3. If the program is still running, **SIGKILL**: the program dies at once,
   exit code 137.

SIGKILL cannot be caught; the program cannot have its last word. The goal is
for the program to close by itself on SIGTERM.

## Catching SIGTERM in Python

```python
import signal
import sys
import time

running = True

def stop(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, stop)

while running:
    print("working", flush=True)
    time.sleep(1)

print("saved, bye", flush=True)
```

The loop checks `running` on every round; when SIGTERM arrives the loop ends,
the last job is done and the program exits with code 0.

## Why `flush=True`?

Python first puts what it prints into a buffer and sends it in batches.
Without a terminal (in a container with `-d`), nothing may appear **until the
buffer fills**; `docker logs` looks empty. Two fixes:

- `print(..., flush=True)`,
- or `ENV PYTHONUNBUFFERED=1` in the image (Environment Variables section).

## What does `--init` do?

`docker run --init` runs a very small starter (`tini`) in the container
before the program. It becomes process number 1; it passes signals on to the
program and collects the "orphan" processes the program leaves behind. A good
solution if you cannot touch your program. In Compose it is written
`init: true`.

## Checklist

- [ ] `CMD` / `ENTRYPOINT` are in the exec form.
- [ ] The program catches SIGTERM (or there is `--init`).
- [ ] Long jobs are split into small pieces; the shutdown request is checked
      between pieces.
- [ ] Output is flushed.
