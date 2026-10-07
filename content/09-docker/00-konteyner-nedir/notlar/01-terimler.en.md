Words that will come up often in this path. You do not need to memorise them
all on the first read; come back to this page when you get stuck.

## Core ideas

| Term | Meaning |
|---|---|
| **Container** | A program that runs in its own small world: it has its own files, packages and settings. |
| **Image** | The mould of a container. An unchanging package on disk; you start as many containers from it as you like. |
| **Dockerfile** | The recipe of an image: which image to start from, which files to copy, which command to run. |
| **Build** | Making an image from a Dockerfile: `docker build`. |
| **Run** | Starting a container from an image: `docker run`. |
| **Instruction** | The upper-case word at the start of each Dockerfile line: `FROM`, `COPY`, `RUN`, `CMD`. |

## About images

| Term | Meaning |
|---|---|
| **Base image** | The ready-made image started from on the `FROM` line, e.g. `python:3.13-slim`. |
| **Tag** | The part of an image name after `:`; usually a version: `3.13-slim` in `python:3.13-slim`. |
| **Layer** | The stacked slices that make up an image; every instruction adds a slice. |
| **Registry** | The place where images are stored and downloaded from. The best known is **Docker Hub**. |
| **Pull** | Downloading an image from a registry: `docker pull`. |

## The parts of Docker

| Term | Meaning |
|---|---|
| **Docker Engine** | The service waiting in the background that actually runs containers (a daemon). |
| **The docker command** (CLI) | The `docker ...` commands you type in the terminal; they tell the Engine what to do. |
| **Docker Desktop** | The desktop program that installs and manages the Engine on Windows and Mac. |
| **Host** | The computer the containers run on; here, your computer. |
| **Kernel** | The bottom part of the operating system; containers share the host's kernel. |

## What you will see later

| Term | Meaning | Section |
|---|---|---|
| **Port** | The door number through which a program in a container is reached from outside. | 07 |
| **Environment variable** | A setting given to the program from outside (`APP_ENV=production`). | 08 |
| **Volume** | A data area that stays even when the container is removed. | 09 |
| **Compose** | A tool that runs several containers together from one file. | 10 |

## Often confused

- **Image ≠ container.** The image is the mould, the container a copy
  started from it. Removing a container does not remove the image.
- **Docker ≠ virtual machine.** A container does not carry a separate
  operating system.
- **Docker Desktop ≠ Docker Engine.** Desktop is only the window that runs
  the Engine on Windows; the Engine does the real work.
