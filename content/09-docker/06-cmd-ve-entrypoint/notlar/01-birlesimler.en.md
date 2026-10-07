How `ENTRYPOINT` and `CMD` behave together. The image contains
`python tool.py`, and the container is run with `docker run image` or
`docker run image x y`.

## The combination table

| Dockerfile | `docker run image` | `docker run image x y` |
|---|---|---|
| `CMD ["python", "tool.py"]` | `python tool.py` | `x y` |
| `ENTRYPOINT ["python", "tool.py"]` | `python tool.py` | `python tool.py x y` |
| `ENTRYPOINT ["python", "tool.py"]` + `CMD ["--help"]` | `python tool.py --help` | `python tool.py x y` |
| `ENTRYPOINT python tool.py` (shell) | `/bin/sh -c "python tool.py"` | `/bin/sh -c "python tool.py"` (x y ignored) |

The last row shows why "do not write a shell-form ENTRYPOINT" is said: the
arguments never arrive.

## Changing it once

| What you want | Command |
|---|---|
| Change `CMD` | `docker run image new command` |
| Change `ENTRYPOINT` | `docker run --entrypoint sh image` |
| Both at once | `docker run --entrypoint python image -c "print(1)"` |

`--entrypoint` only takes the program's name; its arguments are written after
the image name.

## Arguments in Python

```python
import sys

print(sys.argv)
```

`docker run --rm image a b` → `['tool.py', 'a', 'b']`. `sys.argv[0]` is the
file's name, the rest are the arguments. For a tidier command line there is
Python's `argparse` module (it produces `--help` by itself):

```python
import argparse

parser = argparse.ArgumentParser(description="Count words")
parser.add_argument("path")
parser.add_argument("--top", type=int, default=5)
args = parser.parse_args()
```

## Environment variable or argument?

- **Argument:** what changes on every run, the job itself (which file, which
  name).
- **Environment variable:** configuration set once (which database, which
  mode). In the Environment Variables section.
