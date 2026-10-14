**The smallest `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "greeter"
version = "0.1.0"
```

**Commands**

| Command | What it does |
|---|---|
| `python -m pip install build` | Installs the build tool |
| `python -m build` | A wheel (`.whl`) and a source package (`.tar.gz`) into `dist/` |
| `pip wheel . --no-deps -w dist` | Only the wheel (with pip itself) |
| `pip install dist/*.whl` | Installs the wheel |
| `pip install --target folder package.whl` | Installs into a given folder |

**The wheel's name**

```text
greeter-0.1.0-py3-none-any.whl
│       │     │   │    └ platform: every operating system
│       │     │   └ ABI: not tied to Python's internals
│       │     └ Python: any Python 3
│       └ version
└ name
```

For packages with a C extension the last three parts change (e.g.
`cp313-cp313-win_amd64`): a separate wheel is built for each Python
version and operating system; the matrix helps here too.

**Inside**

| File | Contains |
|---|---|
| `greeter/...` | The code itself |
| `greeter-0.1.0.dist-info/METADATA` | Name, version, dependencies |
| `greeter-0.1.0.dist-info/RECORD` | The hash of every file |
| `greeter-0.1.0.dist-info/WHEEL` | The wheel's format information |

**What does a smoke test catch?**

- A file that did not make it into the package (a data file, a
  subpackage).
- An import that is only found when running from the project folder.
- A dependency not written in `pyproject.toml`.
