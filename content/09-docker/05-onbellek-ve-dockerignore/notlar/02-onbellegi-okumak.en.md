The answer to "why does it rebuild from scratch every time?" is in the build
output. How to read it, and the most common causes.

## Signs in the output

| Line | Meaning |
|---|---|
| `#8 CACHED` | The step came from the cache; it was not run. |
| `#8 DONE 0.4s` | The step was run and took 0.4 s. |
| `#8 ERROR: ...` | The step failed; the lines below give the reason. |
| `transferring context: 140B` | The size of the context sent to the engine. |

To find where the cache broke, look at **the first step that says `DONE`**:
everything after it must have run again. Odyssey's terminal also shows the
steps as `CACHED` / `DONE`.

## Why did the cache break? A checklist

1. **A copied file changed.** `COPY . .` breaks when any file in the folder
   changes. Add files whose changes do not matter (`notes.md`, `*.log`) to
   `.dockerignore`.
2. **The order is wrong.** If `COPY . .` comes before `pip install`, every
   code change reinstalls the packages.
3. **The instruction's text changed.** Even a single character outside a
   comment means a new step.
4. **An earlier step changed.** If one link in the chain breaks, all the
   later ones break.
5. **The base image was updated.** If `docker pull python:3.13-slim`
   downloaded a new version, all steps run again. (This is a good thing:
   security fixes arrive too.)
6. **`--no-cache` was given.**

## Breaking the cache on purpose

Sometimes the cache is **not wanted**: `RUN pip install` comes from last
month's cache and you miss a new security fix. Options:

- `docker build --no-cache` → no step comes from the cache (slow).
- `docker build --pull` → download the newest base image, then build.
- Raise the versions in the requirements file → that step and those after it
  run again anyway.

## Where does the cache live?

The cache is kept inside Docker, separately from the images. The **Build
Cache** line in the output of `docker system df` shows how much space it
takes; to clean it up:

```text
docker builder prune
```
