What goes on the `FROM` line for a Python program? Three common options and
which one when.

## Three families

| | `python:3.13` | `python:3.13-slim` | `python:3.13-alpine` |
|---|---|---|---|
| Linux underneath | Full Debian | Trimmed Debian | Alpine |
| Size (unpacked) | ~1 GB | ~180 MB | ~50 MB |
| Build tools (gcc etc.) | Yes | No | No |
| C library | glibc | glibc | musl |
| Package manager | `apt-get` | `apt-get` | `apk` |

## Which one when?

- **`-slim` is usually the best start.** Small, but an ordinary Debian;
  almost all pip packages install smoothly in their pre-built form (wheels).
  This path uses it.
- **The full image (`python:3.13`)**, if a package you install has no
  pre-built form and must be compiled from source. Easy but large; with a
  multi-stage build (later) you get rid of the size.
- **`-alpine`** is the smallest, but watch out: Alpine uses a different C
  library called `musl` instead of `glibc`. Pre-built forms of packages such
  as NumPy and pandas are often for glibc; on Alpine they are compiled from
  source, so installation takes minutes or fails. For pure Python programs
  there is no problem.

## How tightly should the tag be pinned?

| Written as | What happens? |
|---|---|
| `python` | `latest`: a different version at any moment. **Do not write it.** |
| `python:3` | The newest Python 3: 3.13 today, 3.14 tomorrow. |
| `python:3.13-slim` | The newest patch of 3.13 (3.13.16, 3.13.17...). Security fixes arrive, behaviour does not change. **Recommended.** |
| `python:3.13.16-slim` | Exactly this version; no fixes arrive. |
| `python@sha256:...` | Exactly the same image; the most exact. |

For most projects, pinning the "minor version" as in `3.13-slim` is a good
balance: bug fixes arrive automatically, an unexpected major version does
not.

## Processor architecture

Images are built for a particular kind of processor. Most computers are
**amd64** (x86_64); Apple's M series and some new laptops are **arm64**.
Most official images are published for both architectures and Docker picks
the one that matches your computer. If an image does not exist for your
architecture you see this warning:

```text
WARNING: The requested image's platform (linux/arm64) does not match
the detected host platform (linux/amd64)
```

## Ask yourself

1. Is my program pure Python, or are there packages that need compiling?
2. Does the image size matter (will it be downloaded often)?
3. Should everyone on the team use the same version?

The answers usually lead to `python:3.13-slim`.
