# What Is a Container?

You wrote a program and it runs nicely on your computer. You send it to a
friend and it does not start. You put it on a server and it fails. This is
the oldest complaint among developers: **"But it worked on my machine!"**

Docker exists to get rid of that complaint. It puts the program, together
with everything it needs to run, into **a single box**; wherever the box
goes, the program inside runs the same. That box is called a **container**.

We are not installing Docker in this section yet. First we will settle the
ideas: what the problem is, what a container solves and how an image differs
from a container. Installation comes in the next section.

## The problem: a program is never alone

A Python program does not run on its own. Behind it stands an invisible
crowd:

- **Python itself**, and a specific version of it (code that runs on 3.11
  may not run on 3.8),
- **packages** (`pandas`, `requests`...), each in a specific version too,
- **parts of the operating system** (some packages behave differently on
  Linux and on Windows),
- **settings**: environment variables, file paths, open ports.

On your computer all of these happen to be right. On another computer, if one
of them is missing or different, the program breaks. Finding out which one
is different can take hours.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Your computer</h4><p>Python 3.12</p><p>pandas 2.2 installed</p><p>APP_ENV set</p><p><b>Works</b></p></div>
    <div class="no"><h4>The server</h4><p>Python 3.8</p><p>no pandas</p><p>no APP_ENV</p><p><b>Fails</b></p></div>
  </div>
  <figcaption>The code is the same, its surroundings differ. A container removes the difference by carrying the code together with its surroundings.</figcaption>
</figure>

## An analogy: the shipping container

Until the 1950s ships carried cargo piece by piece: sacks, barrels, crates,
each in a different shape. At every port workers unloaded and loaded
everything by hand. In 1956 a **standard steel box** came into use: whatever
you put inside, the outside always has the same size.

Since then cranes, ships, lorries and trains can move the box without knowing
what is inside. The **outside is standard**, the inside is yours.

Docker's container is the same idea. Inside are your program and everything
it needs; the outside is standard. **Every** computer with Docker installed
can open and run this box the same way: your laptop, your friend's computer,
the company server, the cloud.

## What is a container?

A **container** is a program that runs on your computer but **lives in its
own small world**. It has its own files, its own Python, its own packages;
it does not see the other programs on your computer and they do not see it.

What is inside:

- your program (`app.py`),
- the packages the program needs,
- a runtime such as Python,
- the files of a minimal Linux (commands, libraries).

What is **not** inside: a full operating system, a desktop, a separate
kernel. A container shares your computer's kernel; that is why it is small
and fast. A container can start in less than a second.

## How it differs from a virtual machine

"A separate world" brings a **virtual machine** (VM) to mind: an imitation
of a whole computer running inside your computer. A virtual machine does the
job but is heavy, because it carries **an entire operating system**.

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Virtual machine</h4><p>Program</p><p>Packages</p><p><b>A whole operating system</b></p><p>Virtual hardware</p><p>A few GB · minutes</p></div>
    <div class="ok"><h4>Container</h4><p>Program</p><p>Packages</p><p>A few Linux files</p><p><b>Shared kernel</b></p><p>MBs · under a second</p></div>
  </div>
  <figcaption>A virtual machine carries one more operating system every time; a container shares the host's kernel.</figcaption>
</figure>

In short: a virtual machine imitates the **computer**, a container only
separates the **program's surroundings**. Ten virtual machines barely fit on
a server, while hundreds of containers run comfortably.

## Image and container

Two words will come up all the time in Docker, and they are the ones people
mix up most:

- **Image**: the **mould** of a container. It holds the program and
  everything else but does not run; it is a package that sits on disk and
  does not change.
- **Container**: a copy **started** from an image. The live thing that runs
  and can be stopped.

Since you know Python, there is a familiar analogy: an image is a **class**,
a container is an **object** created from that class. Just as you can create
as many book objects as you like from one `Book` class, you can start as
many containers as you like from one image. Each is independent of the
others.

<figure class="fig">
  <div class="flow">
    <span class="node acc">Image: myapp<br><small>mould · class</small></span><span class="arrow">→ docker run →</span>
    <span class="node ok">Container 1</span><span class="node ok">Container 2</span><span class="node ok">Container 3</span>
  </div>
  <figcaption>You can start as many containers as you like from one image; each is separate, what happens in one does not affect the others.</figcaption>
</figure>

## Dockerfile: the recipe of an image

How do you get an image? By writing a recipe. The recipe is called a
**Dockerfile**: a short text file that says "start from this ready-made
image, copy these files, run this command".

```dockerfile
FROM python:3.13-slim
COPY app.py .
CMD ["python", "app.py"]
```

Three lines, three instructions:

- `FROM python:3.13-slim` → start from a ready-made image with Python 3.13
  installed.
- `COPY app.py .` → copy your `app.py` file into the image.
- `CMD ["python", "app.py"]` → when the container runs, run the command
  `python app.py`.

We will learn each line of this recipe one by one later. For now the flow is
what matters:

<figure class="fig">
  <div class="flow">
    <span class="node">Dockerfile<br><small>recipe</small></span><span class="arrow">→ docker build →</span>
    <span class="node acc">Image<br><small>mould</small></span><span class="arrow">→ docker run →</span>
    <span class="node ok">Container<br><small>running program</small></span>
  </div>
  <figcaption>The recipe turns into an image once; the image turns into as many containers as needed.</figcaption>
</figure>

## A first look: commands

You use Docker from the terminal with commands. They all start with the word
`docker`, followed by what to do. Three commands you will run in the next
sections:

```text
docker run hello-world      # run a container from the hello-world image
docker build -t myapp .     # build an image called "myapp" from the Dockerfile here
docker run myapp            # run a container from that image
```

- `run` → "run a container". The name of the image follows.
- `build` → "build an image". `-t myapp` names the image (t: tag); the `.`
  at the end means "the Dockerfile is here, in this folder".

## The parts of Docker

The word "Docker" is actually the shared name of several parts:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Docker Engine</span><span>The service waiting in the background that actually runs containers. It has no window.</span></div>
    <div class="anat-row"><span>The docker command</span><span>The <code>docker run</code>, <code>docker build</code>... you type in the terminal. It tells the Engine what to do.</span></div>
    <div class="anat-row"><span>Docker Desktop</span><span>The desktop program that installs, starts and shows the Engine on Windows and Mac.</span></div>
    <div class="anat-row"><span>Docker Hub</span><span>The website where ready-made images are shared; images such as <code>python</code> and <code>alpine</code> come from there.</span></div>
  </div>
  <figcaption>You type the command, the Engine does the work and downloads the image it needs from Docker Hub.</figcaption>
</figure>

On Windows, containers actually run inside a small, hidden Linux. Docker
Desktop sets it up and manages it for you; you only type `docker` commands.

## Where is Docker used?

- **Shipping software:** an image is sent to the server instead of a
  program. There is no need to install Python or packages on the server.
- **The same environment for a team:** everyone works with the same image,
  so the "it works for me, why not for you" debate is over.
- **Trying ready-made software:** you can run a database with one command
  without installing it, and delete it when you are done.
- **Serving machine learning models:** the model, its libraries and the API
  that serves it sit in one image and give the same result everywhere.

## How we will work in this path

In the exercises you will write a **Dockerfile**, a **compose.yaml** or
**commands**. Odyssey checks what you wrote in two stages:

1. **First it reads the file:** are the instructions right, is the order
   right, is anything missing. This needs no Docker; the exercises of this
   section consist only of this stage.
2. **Then, if Docker is running, it really builds:** it builds the image,
   runs the container and looks at its output. This stage starts in the
   sections after installation.

Everything Odyssey builds is marked `odyssey`; it does not touch your own
images and containers. You can remove the images it built from Settings ›
Docker.

## Summary

- A program is not alone: it also needs a Python version, packages, an
  operating system and settings. The "it worked on my machine" problem comes
  from here.
- A **container** runs a program with everything it needs in a separate
  small world. It is smaller and faster than a virtual machine, because it
  carries only the program's surroundings, not an operating system.
- An **image** is the mould (a class), a **container** a copy started from
  it (an object).
- A **Dockerfile** is the recipe of an image: `docker build` turns the
  recipe into an image, `docker run` turns the image into a container.
