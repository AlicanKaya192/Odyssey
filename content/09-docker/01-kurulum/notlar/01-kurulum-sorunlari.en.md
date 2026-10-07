The most common installation problems and their solutions. Search this page
for part of your error message.

## "Virtualization support not detected" / virtualisation is off

Docker Desktop needs hardware virtualisation.

1. Open Task Manager (Ctrl+Shift+Esc) › **Performance** › **CPU**.
2. If the bottom right says **Virtualization: Disabled**, you need to turn
   it on in the BIOS.
3. While the computer restarts, press the BIOS key (F2, F10, Del or Esc on
   most computers; the start-up screen tells you).
4. The setting's name depends on the manufacturer: **Intel Virtualization
   Technology (VT-x)**, **SVM Mode** (AMD) or **Virtualization**. Set it to
   **Enabled**, save and exit.

## "WSL 2 installation is incomplete" / WSL is outdated

In a PowerShell opened as administrator:

```text
wsl --update
```

If WSL is missing entirely, `wsl --install`. Then restart the computer.

## "'docker' is not recognized as the name of a cmdlet"

The terminal was opened **before** Docker was installed. Close the terminal
windows that were open during installation and open a new one; the new
window finds the `docker` command.

## "failed to connect to the docker API" / "Cannot connect to the Docker daemon"

The `docker` command exists but the engine is not running. This is the most
common message after installation:

```text
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine;
check if the path is correct and if the daemon is running
```

Open Docker Desktop and wait for **Engine running** at the bottom left.
Odyssey says "Docker is not running" in this situation too.

## Docker Desktop stays on "Starting the Docker Engine..."

1. Close Docker Desktop (whale icon › Quit Docker Desktop).
2. Run `wsl --shutdown` in PowerShell (it stops WSL completely).
3. Open Docker Desktop again.

If it does not recover, Docker Desktop › Troubleshoot (the bug icon) ›
**Restart**, or as a last resort **Reset to factory defaults** (it removes
all images and containers).

## `docker pull` hangs or says "TLS handshake timeout"

Images are downloaded from the internet. Check your connection. On a company
or school network a proxy server may block the download; the address your
network administrator gives you goes into Docker Desktop › Settings ›
Resources › Proxies.

## "pull access denied" / "repository does not exist"

The image name is misspelt. `python:3.13-slim` and `python:3.13-slm` are
different things; Docker is looking for an image that does not exist.

## The disk fills up

Images, containers and the build cache take up space. See how much:

```text
docker system df
```

You can remove the images Odyssey built from Settings › Docker. To clean up
stopped containers and unused images left from your own experiments there is
`docker system prune`; it tells you what it will remove and asks for
confirmation. The details are in the Images section.
