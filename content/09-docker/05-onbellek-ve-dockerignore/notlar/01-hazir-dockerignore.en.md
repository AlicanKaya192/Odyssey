A starting `.dockerignore` file for a Python project. Copy it, delete the
lines your project does not have and add your own.

```text
# --- Python ---
**/__pycache__
**/*.pyc
**/*.pyo
.venv
venv
*.egg-info
.pytest_cache
.mypy_cache

# --- Git and the editor ---
.git
.gitignore
.vscode
.idea

# --- Secret settings ---
.env
.env.*
!.env.example

# --- Docker's own files ---
Dockerfile*
compose*.yaml
.dockerignore

# --- Data and output ---
data/
*.log
notebooks/
```

## Why are the lines there?

| Line | Why is it left out? |
|---|---|
| `__pycache__`, `*.pyc` | Python's own cache; the container creates it again anyway. |
| `.venv`, `venv` | The virtual environment on your computer; built for Windows, it does not work in a Linux container and is very large. |
| `.git` | The project's whole history; not needed to run, can be hundreds of MB. |
| `.env` | Passwords, keys. **Must never go into the image.** |
| `!.env.example` | The harmless example file may go in (it shows which settings are needed). |
| `Dockerfile*` | The recipe itself does not need to be in the image. |
| `data/`, `*.log` | Large, often changing files; data is given with a volume (Volumes section). |

## Is it the same as `.gitignore`?

Very similar, but they are separate files and the rules differ a little. The
most important difference: in `.gitignore`, `__pycache__/` applies in every
folder; in `.dockerignore` only at the root. For every folder you need to
write `**/__pycache__`.

## How do you know it works?

Look at the context size in the build output:

```text
#5 transferring context: 140B done
```

If this number is measured in megabytes, something is leaking in. To look
inside the image:

```text
docker run --rm greeter ls -la /app
```
