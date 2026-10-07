`COPY` is the most used instruction, and its small details change the
result. These are the ones met most often.

## The `/` at the end of the destination

```dockerfile
WORKDIR /app
COPY app.py .              # /app/app.py
COPY app.py main.py        # /app/main.py (renamed)
COPY app.py src/           # /app/src/app.py (the src folder is created)
```

If the destination ends with `/`, it counts as a **folder** and the file is
copied into it. If it does not, it counts as the file's **new name**.

## Several files

```dockerfile
COPY app.py utils.py ./    # both to /app
COPY *.py ./               # all .py files
```

With several sources, the destination must be a folder and end with `/`.

## Copying a folder

```dockerfile
COPY src/ ./src/
```

When a folder is copied, **its contents** are copied. If you write
`COPY src/ .`, the contents of `src` are poured straight into `/app`; the
folder itself does not come. To keep the folder, write its name in the
destination too: `./src/`.

## `COPY . .` takes everything

`.` is the whole build context: the `.git` folder, `__pycache__`, the virtual
environment (`.venv`), the `.env` file, large data files... All of them go
into the image. The way to leave out what you do not want is the
`.dockerignore` file; in the next section.

## `COPY` or `ADD`?

`ADD` does everything `COPY` does, plus:

- it unpacks compressed files such as `.tar.gz` while copying,
- it can download a file from an internet address.

These "extra" behaviours cause surprises (it may unpack a file you did not
want unpacked). The rule: **always `COPY`**; `ADD` only when you need to
unpack an archive.

## The source cannot leave the context

```dockerfile
COPY ../shared/config.json .    # not possible
```

No file outside the build context (the folder given to `docker build`) is
visible; you cannot go up with `..`. If needed, make the context one folder
higher and point to the Dockerfile with `-f`:

```text
docker build -f greeter/Dockerfile -t greeter .
```
