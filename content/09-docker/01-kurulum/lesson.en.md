# Installing Docker

This section does one thing: **it installs Docker on your computer and shows
that it works.** By the end you will have run your first container and
downloaded the two images used by every exercise in this path.

Installation is done once and takes 15–30 minutes (mostly downloads and a
restart). Follow the steps in order; if you get stuck somewhere, look at the
"Installation Problems" note of this section.

## What will we install?

On Windows, Docker is called **Docker Desktop**. A single installer brings
all of these:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Docker Engine</span><span>The engine that runs containers. It runs in the background.</span></div>
    <div class="anat-row"><span>The docker command</span><span>The command you will type in the terminal (the Client).</span></div>
    <div class="anat-row"><span>Docker Desktop</span><span>The window that starts and stops the engine and shows its status.</span></div>
    <div class="anat-row"><span>WSL 2</span><span>The small Linux the engine runs in. Docker Desktop sets it up itself.</span></div>
  </div>
  <figcaption>All of them come with one installation; you do not install them one by one.</figcaption>
</figure>

**WSL 2** (Windows Subsystem for Linux) is the Microsoft component that runs
a real Linux kernel inside Windows. Linux containers need a Linux kernel, so
Docker Desktop uses it. It is already present on most up-to-date Windows
installations; if not, the installer guides you.

If you use a Mac, install Docker Desktop for Mac; on Linux, install
**Docker Engine** directly (docs.docker.com/engine/install). All the
commands are the same.

## Requirements

- **Windows 10 (22H2) or Windows 11**, 64-bit.
- **Hardware virtualisation turned on.** In Task Manager › Performance ›
  CPU, the bottom right should say **Virtualization: Enabled**. If it is
  off, it is turned on in the BIOS settings (the note explains how).
- **At least 4 GB of memory**, 8 GB to work comfortably.
- A few GB of free disk space: Docker Desktop ~2 GB, images on top.

Docker Desktop is free for personal use, education and small businesses
(fewer than 250 people and less than 10 million dollars of annual revenue).
If you use it for work at a large company, the company needs a licence.

## Step 1 — Download

1. On **docker.com**, open **Docker Desktop** and press **Download for
   Windows**. (If your computer has an ARM processor choose the "ARM64"
   version; most computers are "AMD64 / x86_64".)
2. The downloaded file is called **Docker Desktop Installer.exe**; it is
   around half a gigabyte.

## Step 2 — Install

1. Double-click **Docker Desktop Installer.exe**. If it asks for
   administrator permission, say **Yes**.
2. On the configuration screen keep **Use WSL 2 instead of Hyper-V
   (recommended)** ticked. "Add shortcut to desktop" is optional.
3. Press **OK**; the files are copied (a few minutes).
4. At the end a **Close and restart** (or "Close and log out") button
   appears. Press it; the computer restarts.

If the installer says WSL is missing or outdated, run this in a PowerShell
opened as administrator, then restart the computer:

```text
wsl --install
```

## Step 3 — First start

1. Open **Docker Desktop** from the Start menu.
2. The **Docker Subscription Service Agreement** window appears; read it and
   press **Accept**.
3. If it asks you to sign in, you can skip with **Skip** or "Continue
   without signing in". A Docker Hub account is not needed for this path.
4. If a short survey appears, you can skip it too.

When Docker Desktop opens, there is a line at the bottom left showing the
engine's status. Wait until you see **Engine running** and the green dot
next to it; on the first start it can take a minute.

<figure class="fig">
<svg viewBox="0 0 640 300" width="640" xmlns="http://www.w3.org/2000/svg">
  <rect class="box" x="1" y="1" width="638" height="298" rx="10"/>
  <text class="ink" x="16" y="23" font-size="13" font-weight="600">Docker Desktop</text>
  <line class="line" x1="1" y1="34" x2="639" y2="34"/>
  <line class="line" x1="150" y1="34" x2="150" y2="268"/>
  <rect class="box" x="10" y="48" width="130" height="24" rx="6"/>
  <text class="ink" x="22" y="64" font-size="12" font-weight="600">Containers</text>
  <text class="dim" x="22" y="94" font-size="12">Images</text>
  <text class="dim" x="22" y="122" font-size="12">Volumes</text>
  <text class="dim" x="22" y="150" font-size="12">Builds</text>
  <text class="ink" x="170" y="66" font-size="16" font-weight="600">Containers</text>
  <text class="dim" x="170" y="100" font-size="11">Name</text>
  <text class="dim" x="290" y="100" font-size="11">Image</text>
  <text class="dim" x="430" y="100" font-size="11">Status</text>
  <text class="dim" x="540" y="100" font-size="11">Port(s)</text>
  <line class="grid" x1="170" y1="108" x2="625" y2="108"/>
  <text class="ink" x="170" y="132" font-size="12">web</text>
  <text class="ink" x="290" y="132" font-size="12">python:3.13-slim</text>
  <circle class="dot3" cx="434" cy="128" r="4"/>
  <text class="ink" x="444" y="132" font-size="12">Running</text>
  <text class="ink" x="540" y="132" font-size="12">8080:8000</text>
  <line class="grid" x1="170" y1="144" x2="625" y2="144"/>
  <text class="ink" x="170" y="168" font-size="12">happy_turing</text>
  <text class="ink" x="290" y="168" font-size="12">hello-world</text>
  <text class="dim" x="430" y="168" font-size="12">Exited</text>
  <line class="line" x1="1" y1="268" x2="639" y2="268"/>
  <circle class="dot3" cx="20" cy="284" r="5"/>
  <text class="ink" x="32" y="288" font-size="12" font-weight="600">Engine running</text>
  <text class="dim" x="150" y="288" font-size="12">← the engine is running</text>
  <text class="dim" x="625" y="288" font-size="11" text-anchor="end">RAM 1.1 GB · CPU 0.4%</text>
</svg>
  <figcaption>A sketch of Docker Desktop. Commands do not work until the green dot and <b>Engine running</b> appear at the bottom left. The Containers list holds running (Running) and finished (Exited) containers.</figcaption>
</figure>

`docker` commands do not work while Docker Desktop is closed. Keep Docker
Desktop open while you work on this path; with Settings › General › **Start
Docker Desktop when you sign in to your computer** you can make it start by
itself when the computer starts.

## Step 4 — Check from the terminal

You will type commands in a terminal. Type **PowerShell** in Start and open
it (it does not need to be an administrator). First ask for the version:

```text
docker version
```

The output has two parts:

```text
Client:
 Version:           29.8.0
 API version:       1.56
 OS/Arch:           windows/amd64
 ...
Server: Docker Desktop 4.92.0 (240144)
 Engine:
  Version:          29.8.0
  OS/Arch:          linux/amd64
  ...
```

- **Client**: the `docker` command you type. `windows/amd64`: it runs on
  Windows.
- **Server**: the Docker Engine running in the background. `linux/amd64`:
  it runs on Linux, that is, inside WSL 2.

Your version numbers may differ; what matters is that both parts appear.

If both appear, the installation is complete. If only Client appears with an
error, Docker Desktop is not open or the engine has not started yet.

## Step 5 — The first container

Now run a real container:

```text
docker run hello-world
```

The first time, this happens:

<figure class="fig">
  <div class="flow">
    <span class="node">1. No image<br><small>Unable to find</small></span><span class="arrow">→</span>
    <span class="node">2. Downloading<br><small>Pulling…</small></span><span class="arrow">→</span>
    <span class="node acc">3. Running<br><small>the program prints</small></span><span class="arrow">→</span>
    <span class="node ok">4. Done<br><small>it stops</small></span>
  </div>
  <figcaption>If <code>docker run</code> cannot find the image, it downloads it first. When the program ends, the container ends too (Exited).</figcaption>
</figure>

If you see a few paragraphs starting with `Hello from Docker!`, Docker is
working. Run the command once more: this time the "Unable to find image"
line does not appear, because the image is now on your computer.

## Step 6 — Download the path's two images

All the exercises of this path use only two **base images**. Download both
once now; in the following sections the exercises work even without an
internet connection:

```text
docker pull python:3.13-slim
docker pull alpine:3.22
```

- `pull` → download (pull) an image from Docker Hub.
- `python:3.13-slim` → a Linux with Python 3.13 installed and unneeded parts
  removed ("slim"). ~45 MB is downloaded, ~180 MB once unpacked.
- `alpine:3.22` → a very small Linux, ~4 MB.

List what you downloaded:

```text
docker images
```

```text
IMAGE              ID             DISK USAGE   CONTENT SIZE   EXTRA
alpine:3.22        5291449c3df7       12.8MB         3.88MB
python:3.13-slim   bf44cdfcb76c        178MB         45.3MB
```

- **ID**: the first 12 characters of the image's identity.
- **DISK USAGE**: the space its unpacked form takes on disk.
- **CONTENT SIZE**: the downloaded (compressed) size.

The list also contains `hello-world`, a few KB. The column names may differ
slightly between Docker versions (older versions show `REPOSITORY`, `TAG`,
`SIZE`); what matters is that the images are in the list.

## How does Odyssey find Docker?

You do not need to set anything up. Odyssey finds the `docker` command by
itself and checks whether the engine is running when you press "Run". You
can see the status on the Settings › **Docker** page: a line such as
"Docker 29.8.0 is running" and the total of the images Odyssey has built.

If you run an exercise while Docker is closed, Odyssey still reads and
checks your Dockerfile but cannot build the image; a "Docker is not running"
warning appears in the terminal. Opening Docker Desktop and running again is
enough.

## Closing and uninstalling

- **Closing:** right-click the whale icon on the right of the taskbar ›
  **Quit Docker Desktop**. Closing the window does not stop the engine; it
  keeps running in the background.
- **Uninstalling:** Windows Settings › Apps › Docker Desktop › Uninstall.
  Images and containers go too.

## Summary

- On Windows, Docker = **Docker Desktop**; behind it is a Linux kernel
  running with WSL 2.
- Needed: 64-bit Windows 10/11, virtualisation on, 4–8 GB of memory.
- `docker` commands do not work until **Engine running** appears at the
  bottom left.
- `docker version` shows the Client and the Server, `docker run hello-world`
  the first container, `docker pull` downloading an image, `docker images`
  what has been downloaded.
- The path's two images: `python:3.13-slim` and `alpine:3.22`.
