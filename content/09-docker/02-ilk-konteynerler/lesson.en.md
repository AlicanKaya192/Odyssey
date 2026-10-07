# Your First Containers

During installation you ran your first container with `hello-world`: it
started, printed a message and stopped. In this section we will really play
with containers: we will go inside them, run them in the background, stop and
restart them and remove them.

Run this section's commands in PowerShell yourself as well. Containers do
not harm your computer; at worst you remove them and start again.

## Giving a container a command

If you write a command after the image name in `docker run`, the container
runs that command:

```text
docker run alpine:3.22 echo "Hello container"
```

```text
Hello container
```

Here is what happened: Docker created a new container from the `alpine:3.22`
image, ran the `echo` command inside it, the command finished and so did the
container.

**A container lives as long as the program inside it runs.** When the
program ends, the container stops too. This is the most important sentence
of this section.

Everything after the image name is the command to run inside the container:

```text
docker run alpine:3.22 ls /
docker run alpine:3.22 cat /etc/os-release
docker run python:3.13-slim python -c "print(2 ** 10)"
```

## Listing containers

`docker ps` shows the running containers (ps: process status):

```text
docker ps
```

The ones you just ran are not in the list, because they have all finished.
To see **all of them, finished ones included**, use `-a` (all):

```text
docker ps -a
```

```text
CONTAINER ID   IMAGE              STATUS                     NAMES
7c80c00c94a5   python:3.13-slim   Exited (0) 5 seconds ago   eager_hopper
3f1d2b9a6e44   alpine:3.22        Exited (0) 9 seconds ago   jolly_lamport
```

The real output also has `COMMAND` (the command run), `CREATED` (when it was
created) and `PORTS` columns; we left them out here so it fits.

- **CONTAINER ID**: the container's identity (its first 12 characters).
- **STATUS**: `Exited (0)` → finished, exit code 0 (no problem).
  `Up 3 minutes` → running.
- **NAMES**: the name. If you do not give one, Docker picks two random words.

Finished containers stay there until they are removed. Every `docker run`
creates a **new** container; run the same command ten times and there are
ten containers in the list.

## Naming and removing automatically

To avoid dealing with random names, use `--name`:

```text
docker run --name greeter alpine:3.22 echo hi
```

Two containers cannot have the same name; if you run the same command again
without removing the old one, you get this error:

```text
docker: Error response from daemon: Conflict. The container name "/greeter"
is already in use by container "ed8f7979...". You have to remove (or rename)
that container to be able to reuse that name.
```

If you do not want trial containers to pile up, use `--rm`: the container is
**removed automatically** when it finishes.

```text
docker run --rm alpine:3.22 echo "leaving no trace"
```

## Going inside: `-it`

You can open a terminal inside a container. In Alpine the shell (command
interpreter) program is called `sh`:

```text
docker run -it --rm alpine:3.22 sh
```

- `-i` (interactive): pass what you type on the keyboard to the container.
- `-t` (tty): give it a terminal (so the command line looks right).
- The two are always used together, so they are written as `-it`.

The prompt changes; you are now inside the container:

```text
/ # ls
bin    dev    etc    home   lib    media  mnt    opt    proc
root   run    sbin   srv    sys    tmp    usr    var
/ # cat /etc/os-release
NAME="Alpine Linux"
...
/ # exit
```

When you type `exit`, the shell ends, so the container ends too (and since
you gave `--rm`, it is removed as well).

## A container is disposable

Try this:

```text
docker run -it --rm alpine:3.22 sh
/ # echo "note" > /note.txt
/ # cat /note.txt
note
/ # exit

docker run -it --rm alpine:3.22 sh
/ # cat /note.txt
cat: can't open '/note.txt': No such file or directory
```

The second container is **from the same image but new**; the file you wrote
in the first one is not in it. The image does not change; a change you make
inside a container exists only in that container, and disappears when it is
removed.

<figure class="fig">
  <div class="flow">
    <span class="node acc">Image: alpine:3.22<br><small>unchanging, read-only</small></span><span class="arrow">→</span>
    <span class="node">Container 1<br><small>/note.txt written</small></span><span class="arrow">→ removed →</span>
    <span class="node no">The note is gone</span>
  </div>
  <figcaption>Each container adds its own thin, writable layer on top of the image. When the container is removed, that layer goes too; the image always stays the same.</figcaption>
</figure>

How is lasting data kept? In the Volumes section. For now the rule is:
**do not write anything important into a container; a container should be
removable and re-creatable at any moment.**

## Running in the background: `-d`

Some programs never finish: a web server, a database. To run them in the
background without locking the terminal, use `-d` (detached):

```text
docker run -d --name sleeper alpine:3.22 sleep 300
```

```text
3b8f6c1e0a9d4f27c5e1b2a3d4c5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3
```

Docker only prints the container's long identity and gives the terminal back
to you. `sleep 300` is a command that waits 300 seconds; during that time the
container is **running**:

```text
docker ps
```

```text
CONTAINER ID   IMAGE         STATUS          NAMES
3b8f6c1e0a9d   alpine:3.22   Up 12 seconds   sleeper
```

## Talking to a running container

**Seeing its output** (`logs`):

```text
docker logs sleeper
docker logs -f sleeper      # -f: follow live (leave with Ctrl+C)
```

**Running a command inside it** (`exec`): it starts a second command inside
the running container.

```text
docker exec sleeper ps
```

```text
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 300
    7 root      0:00 ps
```

There are only two programs inside the container: `sleep 300` as process
number 1 (the container's main program) and the `ps` you ran. The hundreds
of programs on your computer are not visible from here; this is the
container's "own world".

Going inside with a shell works the same way:

```text
docker exec -it sleeper sh
```

`run` creates a new container; `exec` runs a command inside an **existing,
running** container. These two are the pair people confuse.

## Stopping, starting, removing

```text
docker stop sleeper     # stop (gives the program at most 10 s to shut down)
docker start sleeper    # start a stopped container again
docker rm sleeper       # remove (it must be stopped first)
docker rm -f sleeper    # force-stop and remove even if it is running
```

If you try to remove a running container without `-f`, Docker asks you to
stop it: `container is running: stop the container before removing or force
remove`.

You can refer to a container by its name or by the first few characters of
its identity (`docker stop 3b8f`).

<figure class="fig">
  <div class="flow">
    <span class="node">Image</span><span class="arrow">→ run →</span>
    <span class="node ok">Running<br><small>Up</small></span><span class="arrow">→ stop →</span>
    <span class="node">Stopped<br><small>Exited</small></span><span class="arrow">→ rm →</span>
    <span class="node no">Removed</span>
  </div>
  <figcaption>A container also stops when its program ends by itself. A stopped container runs again with <code>start</code>; <code>rm -f</code> removes even a running one directly.</figcaption>
</figure>

## Cleaning up in bulk

If your experiments have piled up, to remove all stopped containers:

```text
docker container prune
```

Docker tells you what it will remove and asks for confirmation. It does not
touch running containers.

## Summary

- `docker run image command` → creates a new container and runs the
  command. **When the program ends, the container ends too.**
- `docker ps` lists the running ones, `docker ps -a` all of them.
- `--name name` names it, `--rm` removes it when it ends, `-it` goes
  inside, `-d` runs it in the background.
- `logs` shows the output, `exec` runs a command in a running container.
- `stop` / `start` / `rm` (`-f` to force); `docker container prune` cleans
  up the stopped ones.
- A container is disposable: what you write inside it disappears when it is
  removed; the image does not change.
