Docker Desktop is not only the window that runs the engine; it also shows the
result of the commands you type in the terminal visually. Everything you do
with commands in this path can be followed here too.

## The left menu

| Section | What does it show? | Terminal equivalent |
|---|---|---|
| **Containers** | Running and stopped containers: name, image, status, ports. | `docker ps -a` |
| **Images** | The images on the computer and their sizes. | `docker images` |
| **Volumes** | Data areas that stay even when a container is removed. | `docker volume ls` |
| **Builds** | The `docker build` history: how long each step took, which came from the cache. | `docker build` output |

## A container row

In the Containers list, each container's row has:

- **Name**: the container's name (if you do not give one, Docker picks two
  random words, e.g. `happy_turing`).
- **Image**: which image it was started from.
- **Status**: `Running` or `Exited` (finished).
- **Port(s)**: a clickable link if a port is open to the outside.
- **Stop / start / delete** buttons on the right.

Clicking the row opens the container's **Logs** (its output), **Inspect**
(its settings), **Exec** (running a command inside it) and **Files** (its
files) tabs. They are very useful when debugging; we will see their terminal
equivalents in the Debugging section.

## The bottom bar

- **Engine running** and a green dot at the bottom left: the engine is
  running.
- Next to it, memory and processor usage.

## Settings (the gear at the top right)

- **General › Start Docker Desktop when you sign in**: start automatically
  when the computer starts.
- **Resources**: the memory and processor Docker may use (with WSL 2,
  Windows manages these limits).
- **Docker Engine**: the engine's configuration file. Do not change it
  without knowing what you are doing.

## The whale in the taskbar

There is a small whale icon on the right of the taskbar. Right-click it:

- **Quit Docker Desktop**: stops the engine and quits.
- **Restart**: restarts the engine.
- **Dashboard**: opens the window.

Closing the Docker Desktop window with the cross **does not stop** the
engine; your containers keep running.

## Commands or the window?

Both do the same job. In this path we learn the **commands**, because:

- servers have no windows, only a terminal,
- commands can be written to a file and repeated,
- error messages are clearer in the terminal.

Use Docker Desktop to take a quick look at "what happened?".
