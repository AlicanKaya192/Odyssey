# The Build Cache and .dockerignore

The first `docker build` takes a while; when you make a small change to the
code and build again, the build finishes in a second. The reason is the
**build cache**. Understanding the cache is the answer to why we write a
Dockerfile in a particular order. In this section we will also learn to leave
out files that **must not go into** the image.

## How does the cache work?

Before running each instruction, Docker asks: **"Have I done this exact step
before?"**

- Is the instruction's text the same?
- Is the previous step the same?
- If it is a `COPY`, are the **contents** of the copied files the same?

If yes, it does not run the step again; it takes last time's layer and writes
`CACHED` in the output. If not, it runs the step.

The critical rule: **when a step changes, every step after it runs again
too.** Layers are stacked; when a lower one changes, the ones above become
invalid.

<figure class="fig">
  <div class="flow">
    <span class="node ok">FROM<br><small>CACHED</small></span><span class="arrow">→</span>
    <span class="node ok">WORKDIR<br><small>CACHED</small></span><span class="arrow">→</span>
    <span class="node no">COPY . .<br><small>changed</small></span><span class="arrow">→</span>
    <span class="node no">RUN pip install<br><small>again</small></span><span class="arrow">→</span>
    <span class="node no">CMD<br><small>again</small></span>
  </div>
  <figcaption>When one link of the chain changes, every step after it runs again. Put expensive steps <b>before</b> the steps that change.</figcaption>
</figure>

## The right order: what happens when the code changes?

The skeleton from the previous section:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

When you change a line in `app.py` and build again (output shortened):

```text
#7 [2/5] WORKDIR /app
#7 CACHED
#6 [3/5] COPY requirements.txt .
#6 CACHED
#8 [4/5] RUN pip install --no-cache-dir -r requirements.txt
#8 CACHED
#9 [5/5] COPY . .
#9 DONE 0.0s
```

Since `requirements.txt` did not change, the pip step came **from the
cache**; only the last `COPY` ran again. (The steps are prepared in parallel,
so the order in the output is a little mixed; look at the number in square
brackets.)

## The wrong order: the same change

Now let us try the shortcut: copy everything at once, then install.

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```

The same small change to `app.py`:

```text
#6 [2/4] WORKDIR /app
#6 CACHED
#7 [3/4] COPY . .
#7 DONE 0.0s
#8 [4/4] RUN pip install --no-cache-dir -r requirements.txt
#8 DONE 1.2s
```

`COPY . .` changed because it copies `app.py` too; the pip step after it ran
**again** as well. Here it is 1.2 seconds because the list has no packages. A
real project has pandas, scikit-learn and dozens of packages; that means
**minutes** of reinstalling on every code change.

## The rule: rarely changing first, often changing last

Write the Dockerfile **from what changes least to what changes most**:

1. The base image (changes a few times a year)
2. System packages
3. `requirements.txt` and `pip install` (a few times a month)
4. The code itself (dozens of times a day)

That was the reason for the two separate `COPY` lines: first only the
dependency list, then the code.

## `RUN`'s cache looks at the text

A `RUN` step's cache looks only at **the command's text** (and the previous
steps); it does not know what changed in the outside world. This is
surprising in two places:

```dockerfile
RUN apt-get update
RUN apt-get install -y curl
```

The first line ran once and went into the cache. Months later, when you add a
new package to the second line, the first line still comes from the cache;
the package list is months old and the installation can fail. The fix: join
the two in **one `RUN`**.

```dockerfile
RUN apt-get update && apt-get install -y curl
```

If you need to ignore the cache entirely:

```text
docker build --no-cache -t greeter .
```

## The build context and `.dockerignore`

When `docker build .` starts, it sends the **whole** folder to the engine:

```text
#5 transferring context: 5.00MB 0.3s done
```

The folder had a 5 MB data file and a `.git` folder. All of it was sent, and
with `COPY . .` it went into the image as well. In large projects this
becomes hundreds of MB.

Worse: the **`.env`** file in the folder (passwords, API keys) goes into the
image. Everyone you share the image with gets it too.

The fix is to put a file called **`.dockerignore`** next to the Dockerfile.
Files matching the patterns in it never enter the context:

```text
# Python (in every folder)
**/__pycache__
**/*.pyc
.venv

# Git
.git

# Secret settings
.env

# Large data
data/
```

In the same folder again:

```text
#5 transferring context: 140B done
```

From 5 MB to 140 bytes. `COPY . .` can no longer see these files.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>No .dockerignore</h4><p>app.py, requirements.txt</p><p>.git/ (history)</p><p>.env (passwords!)</p><p>data/ (5 MB)</p><p><b>context: 5.00 MB</b></p></div>
    <div class="ok"><h4>With .dockerignore</h4><p>app.py, requirements.txt</p><p><b>context: 140 B</b></p><p>no secrets, no data</p></div>
  </div>
  <figcaption>A file that does not enter the context cannot enter the image with <code>COPY . .</code> either.</figcaption>
</figure>

## `.dockerignore` patterns

| Pattern | What is left out? |
|---|---|
| `.env` | The `.env` file at the root |
| `*.pyc` | All `.pyc` files at the root |
| `**/*.pyc` | `.pyc` files in every folder |
| `**/__pycache__` | `__pycache__` in every folder |
| `data/` or `data` | The `data` folder at the root and its contents |
| `!data/sample.csv` | An **exception** to the previous rule: this file goes in |
| `# ...` | A comment |

Patterns are read relative to the root of the build context. `__pycache__`
only leaves out the folder at the root; `app/__pycache__` needs `**/`.

There is one more benefit: when a file that is left out changes, the
`COPY . .` cache **does not break**. For example, if you write `notes.md` in
`.dockerignore`, editing your note does not restart the build.

## Summary

- At every step Docker asks "have I done this before?"; if yes, `CACHED`.
- **When a step changes, all the steps after it run again.**
- Write what changes rarely first and what changes often last: first
  `requirements.txt` + `pip install`, then `COPY . .`.
- `RUN`'s cache looks at the text; join `apt-get update` and `install` in one
  `RUN`. `--no-cache` ignores the cache.
- `.dockerignore` decides what stays out of the context: `.git`, `.venv`,
  `__pycache__`, `.env`, large data. The image gets smaller, secrets do not
  leak and the cache does not break needlessly.
