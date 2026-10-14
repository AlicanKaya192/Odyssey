# Artifacts and Packaging

So far our pipeline produced a **decision**: the tests passed or failed.
But a pipeline can also have a **product**: an installable package, a
test report, a coverage report. These files are lost with the job's
machine; we saw in the fifth section that jobs do not share files. In
this section we see how to keep the files a pipeline produces
(**artifacts**), how to move them between jobs, and how to turn a Python
project into an installable package.

## What is an artifact?

An **artifact** is a file or folder that a run produces and that is
stored on GitHub. It can be downloaded as a zip from the run's page and
picked up by another job in the same run. Two actions work with it:

```yaml
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

```yaml
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
```

- `upload-artifact`: stores the `path` folder (or its files) under the
  name `name`.
- `download-artifact`: downloads what was stored under that name to this
  job's machine, into the `path` folder. If `name` is not written, all
  of the run's artifacts are downloaded.

Do not confuse it with the cache:

<figure class="fig versus">
  <div><h4>Cache</h4>For speed. Found by a key, shared between runs, may disappear; the job must work correctly without it.</div>
  <div><h4>Artifact</h4>For the product. Belongs to a run, found by name, downloadable from the page; it stays until its retention ends.</div>
  <figcaption>A cache says "let us not download again", an artifact says "let us keep this".</figcaption>
</figure>

Artifacts are kept for 90 days by default; this can be shortened with
`retention-days`. Every stored byte counts against the repository's
storage quota (in private repositories); a few days are enough for
short-lived files like a test report.

## A Python package: the wheel

Making a Python project installable by someone else with `pip install`
is called **packaging**. The project's name, version and how it is built
are written in the `pyproject.toml` file:

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "greeter"
version = "0.1.0"
```

The product of the build is a **wheel** file: a zip with the `.whl`
extension, containing the package's files and information. Let us set up
a small project, really build its wheel and look inside. Since this
computer works offline, we build with pip's own wheel command; in
pipelines on GitHub `python -m build` is usually used instead, and the
product has the same form.

```python
import subprocess
import sys
import zipfile
from pathlib import Path

project = Path("greeter-project")
(project / "greeter").mkdir(parents=True)
(project / "greeter" / "__init__.py").write_text(
    'def hello():\n    return "Hello from greeter"\n')
(project / "pyproject.toml").write_text(
    '[build-system]\nrequires = ["setuptools"]\n'
    'build-backend = "setuptools.build_meta"\n\n'
    '[project]\nname = "greeter"\nversion = "0.1.0"\n')

subprocess.run([sys.executable, "-m", "pip", "wheel", ".", "--no-deps",
                "--no-build-isolation", "-w", "dist", "-q"],
               cwd=project, check=True)
wheel = next((project / "dist").iterdir())
print(wheel.name)
for name in sorted(zipfile.ZipFile(wheel).namelist()):
    print("  " + name)
```

```text
greeter-0.1.0-py3-none-any.whl
  greeter-0.1.0.dist-info/METADATA
  greeter-0.1.0.dist-info/RECORD
  greeter-0.1.0.dist-info/WHEEL
  greeter-0.1.0.dist-info/top_level.txt
  greeter/__init__.py
```

The file's name carries its own information:

<figure class="fig anat">
  <div class="anat-row"><span><code>greeter</code></span><span>The package's name.</span></div>
  <div class="anat-row"><span><code>0.1.0</code></span><span>The version (in the tenth section).</span></div>
  <div class="anat-row"><span><code>py3</code></span><span>Which Python: any Python 3.</span></div>
  <div class="anat-row"><span><code>none</code></span><span>No C extension, not tied to Python's internals.</span></div>
  <div class="anat-row"><span><code>any</code></span><span>Works on every operating system.</span></div>
</figure>

Inside are the code itself (`greeter/__init__.py`) and, in the
`dist-info` folder, the package's information: `METADATA` its name and
version, `RECORD` the hash of every file (at installation this is how it
is checked that the files are not corrupted).

## Does it work once installed?

Passing tests do not mean the package is right too: a file may not have
made it into the package, the code may depend on something that is only
found when it runs from the project folder. A **smoke test** installs the
package in a clean place and checks whether it does its most basic job.
Let us install the wheel above into an empty folder and import it from
there:

```python
target = Path("clean-install")
subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "-q",
                "--target", str(target), str(wheel)], check=True)
result = subprocess.run(
    [sys.executable, "-c", "import greeter; print(greeter.hello())"],
    cwd=target, capture_output=True, text=True)
print(result.stdout.strip())
print(sorted(path.name for path in target.iterdir()))
```

```text
Hello from greeter
['greeter', 'greeter-0.1.0.dist-info']
```

The package ran outside the project folder, only from the installed
files. Its counterpart in a pipeline is a separate job: it takes the
wheel as an artifact, installs it on a clean machine and tries a
command.

## Build once, use the same one

An important rule of a pipeline: **the package is built once; what is
tested, deployed and released is always that file.** Building again in
every job opens the chance that the tested file and the released file
are different (a dependency may have released a new version in the
meantime). Artifacts make this possible: the build job uploads, the
other jobs download.

The **SHA-256 hash** shows that the moved file did not change. That is
why released packages come with their hashes:

```python
import hashlib


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


original = sha256_of(wheel)
copy = Path("downloaded.whl")
copy.write_bytes(wheel.read_bytes())
print("same file:   ", sha256_of(copy) == original)

data = bytearray(copy.read_bytes())
data[100] ^= 1
copy.write_bytes(bytes(data))
print("one bit flip:", sha256_of(copy) == original)
```

```text
same file:    True
one bit flip: False
```

Even a single changed bit makes the hash completely different.

## Packaging in the pipeline

```yaml
name: Package

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7
  smoke-test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: pip install dist/*.whl
      - run: python -c "import greeter; print(greeter.hello())"
```

- `python -m build` writes the wheel and the source package (`.tar.gz`)
  into the `dist/` folder.
- The `smoke-test` job has **no** `checkout`: it uses only the package,
  not the code. If the package is broken because of a missing file, it
  shows up here.

## Keeping the test report

When tests fail the details stay in the log, but scrolling through a long
log is hard. pytest can also write the result to a file; that file is
kept as an artifact. What matters is to keep it **when the tests fail
too**; otherwise there is no report exactly when it is needed most. The
`always()` from the fifth section works at the step level too:

```yaml
      - run: python -m pytest --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-report
          path: report.xml
          retention-days: 14
```

Two artifacts with the same name cannot be uploaded in one run. If every
job in a matrix uploads its own report, the name comes from the matrix:
`name: report-${{ matrix.os }}`.

## Next

We built the package, tested it, kept it. **Releasing** it with a version
number (a GitHub release, a package index) needs permissions and
secrets; those are in the ninth (secrets) and tenth (versioning)
sections.

## Summary

- An artifact is a stored file a run produces; it is moved between jobs
  with `upload-artifact` / `download-artifact`.
- A cache is for speed, an artifact for the product.
- `pyproject.toml` defines the package; the product is a `.whl` wheel (a
  zip). Its name: name, version, Python, ABI, platform.
- A smoke test installs the package in a clean place and tries it.
- Build once; the tested and the released file should be the same. The
  SHA-256 hash shows the file did not change.
- Keep the report with `if: always()`; in a matrix, take its name from
  the matrix.
