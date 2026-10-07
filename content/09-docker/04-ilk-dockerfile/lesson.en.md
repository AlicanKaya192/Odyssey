# Your First Dockerfile

The Dockerfiles so far were two or three lines long. In this section we will
write a Dockerfile that packages a real Python project, knowing the reason
for every line. The rest of the path will be built on this skeleton.

## The project

There are three files in the folder:

```text
greeter/
├── app.py
├── requirements.txt
└── Dockerfile
```

`app.py` is the program itself, `requirements.txt` the list of packages it
needs (empty for now), and `Dockerfile` the recipe:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Six lines, five different instructions. Let us look at them one by one.

## `FROM`: where do we start?

```dockerfile
FROM python:3.13-slim
```

Every Dockerfile starts with `FROM`: the **base image** the image is built
on. We do not bother installing Python; we start from a ready-made image with
Python installed. The version is pinned (`3.13-slim`, not `latest`).

## `WORKDIR`: the working folder

```dockerfile
WORKDIR /app
```

It creates the `/app` folder inside the image and **goes into it**; all the
following instructions run there. Like `cd` in the terminal, but it also
creates the folder if it does not exist.

Why is it needed? Without `WORKDIR` everything goes to the image's root folder
(`/`); your files get mixed with Linux's `bin`, `etc` and `usr` folders. Your
own folder is tidy and predictable.

## `COPY`: bringing files into the image

```dockerfile
COPY requirements.txt .
COPY . .
```

`COPY source destination`:

- **source**: a file on your computer, relative to the folder the Dockerfile
  is in.
- **destination**: the place inside the image. `.` means "the working
  folder", that is, `/app`.

`COPY . .` means "copy everything here to `/app`". So why do we first copy
only `requirements.txt` and then everything? The answer is in the next
section, in the build cache. For now, let the order be like this.

## `RUN`: running a command during the build

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

`RUN` runs a command **while the image is being built** and saves the result
into the image as a new layer. Here we install the packages listed in
`requirements.txt`; the installed packages stay inside the image.

`--no-cache-dir` tells pip not to keep a copy of the files it downloads. That
cache is useful on your computer but only takes up space in an image.

## `CMD`: when the container runs

```dockerfile
CMD ["python", "app.py"]
```

The command that runs when the container is **started**. Only one `CMD` takes
effect in a Dockerfile; if you write several, the last one wins.

## The most important distinction: `RUN` and `CMD`

<figure class="fig">
  <div class="versus">
    <div><h4>RUN</h4><p><b>When:</b> while the image is built (<code>docker build</code>)</p><p><b>How often:</b> once per build</p><p><b>Result:</b> goes into the image as a new layer</p><p><b>How many:</b> as many as you like</p><p><b>Example:</b> installing packages</p></div>
    <div class="ok"><h4>CMD</h4><p><b>When:</b> when the container runs (<code>docker run</code>)</p><p><b>How often:</b> once per container</p><p><b>Result:</b> the program's output</p><p><b>How many:</b> only the last one counts</p><p><b>Example:</b> starting the program</p></div>
  </div>
  <figcaption><code>RUN</code> prepares the image, <code>CMD</code> tells the container what to do.</figcaption>
</figure>

A common mistake: trying to run the program with `RUN python app.py`. That
line runs the program **once, while the image is being built**, not when the
container starts.

## Building and running

From inside the folder:

```text
docker build -t greeter .
```

The output (slightly shortened):

```text
#5 [1/5] FROM docker.io/library/python:3.13-slim@sha256:bf44cdfc...
#6 [2/5] WORKDIR /app
#7 [3/5] COPY requirements.txt .
#8 [4/5] RUN pip install --no-cache-dir -r requirements.txt
#8 1.466 WARNING: Running pip as the 'root' user can result in broken permissions...
#9 [5/5] COPY . .
#10 naming to docker.io/library/greeter:latest done
```

- Each `[n/5]` line is an instruction in the Dockerfile (five steps, FROM
  included).
- pip's "root" warning is harmless here: nothing else inside the container
  breaks. In the Security section we will learn to run the image as a
  non-root user.
- The last line: the image was saved as `greeter:latest` (`latest` was added
  because `-t greeter` has no tag).

Run it:

```text
docker run --rm greeter
```

```text
Hello from the greeter
```

## The build context

The last `.` in the command is the **build context**: the folder sent to
Docker. When the build starts, the whole folder is passed to the engine (the
`transferring context` line), and `COPY` can only take files from **inside**
this folder.

If you ask for a file outside the context, or misspell its name:

```text
COPY app.pyy .
```

```text
ERROR: failed to build: failed to solve: failed to compute cache key:
failed to calculate checksum of ref ...: "/app.pyy": not found
```

The end of the error is what matters: `"/app.pyy": not found` → there is no
such file in the context.

## Dockerfile writing rules

- Instructions are written in **upper case** (`FROM`, `COPY`). Lower case
  works too, but the habit is upper case.
- One instruction per line. A long line is split by putting `\` at the end.
- A line starting with `#` is a comment.
- The file is called `Dockerfile` (no extension, capital D). If you used
  another name, point to it with `docker build -f Dockerfile.dev .`.

## Summary

- The skeleton: `FROM` → `WORKDIR` → `COPY requirements.txt` →
  `RUN pip install` → `COPY . .` → `CMD`.
- `WORKDIR` creates your own folder and goes into it; files do not scatter
  over `/`.
- `COPY source destination`; the source from inside the build context, the
  destination inside the image (`.` = the working folder).
- **`RUN` during the build, `CMD` when the container runs.**
- `docker build -t name .` builds (`.` is the build context),
  `docker run --rm name` runs.
- A `"...": not found` error: the file is not in the context or its name is
  wrong.
