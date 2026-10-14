# Caching and Speed

The slower the pipeline, the less often it is run, and the developer
moves on to something else while waiting for the result; feedback comes
late. Since each job starts on a clean machine, most of the time goes to
work that is **done from scratch every time**: installing Python,
downloading packages. In this section we see how to skip repeated work
with a **cache**, how to cancel old runs, and the other ways to speed up
a pipeline.

## Where does the time go?

The steps of a typical test job:

1. Preparing the machine and getting the code.
2. Installing Python.
3. Downloading and installing the dependencies (`pip install`).
4. Running the tests.

The third step is often the longest, and every run downloads the
**same** packages from the same place. If `requirements.txt` did not
change, the result does not change either: it is possible to keep what
the previous run downloaded and use it again.

## How does a cache work?

The `actions/cache` action stores a folder under a **key**:

```yaml
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            pip-${{ runner.os }}-
```

- **When the step runs**, it looks for a cache stored under this key. If
  it finds one, it restores the `path` folder.
- **When the job finishes successfully**, if the key is being used for
  the first time, it stores the folder under that key.
- `~/.cache/pip` is the folder where pip keeps the packages it downloads
  (on Linux). If the cache is full, `pip install` takes the packages from
  there instead of the internet.

The cache step must come **before** the installation; a restored folder
is only useful to the steps after it.

## Making the key from the content

The most important rule of the key: **when what is stored changes, the
key must change too.** Otherwise old packages are restored forever.
`hashFiles('requirements.txt')` produces a **hash** from the file's
content; if the content is the same the hash is the same, if one letter
changes it is completely different. GitHub uses SHA-256 for this. Let us
see the same idea in Python:

```python
import hashlib


def cache_key(runner_os, requirements):
    digest = hashlib.sha256(requirements.encode()).hexdigest()
    return "pip-" + runner_os + "-" + digest[:12]


before = "pytest==8.4.2\nrequests==2.32.5\n"
after = "pytest==8.4.2\nrequests==2.32.6\n"
print(cache_key("Linux", before))
print(cache_key("Linux", before))
print(cache_key("Linux", after))
print(cache_key("Windows", before))
```

```text
pip-Linux-74c0ae9e3910
pip-Linux-74c0ae9e3910
pip-Linux-84b35b85d419
pip-Windows-74c0ae9e3910
```

- The same content → the same key: the second run finds the cache.
- One version number changed → a new key: the old packages are not used.
- The operating system is in the key too: packages downloaded on Windows
  do not fit Linux, they must not mix. In a workflow, `runner.os` is the
  machine's operating system (`Linux`, `Windows`, `macOS`).

## restore-keys: a partial match

When a single line of `requirements.txt` changes, the full key does not
match and the cache is wasted entirely; yet most packages are the same.
`restore-keys` is a list of fallback **prefixes**: if the full key is not
found, the **newest** cache starting with each prefix, in order, is
restored. pip downloads only the missing packages. Let us write the rule
in Python (`saved` goes from oldest to newest):

```python
def restore(key, restore_keys, saved):
    if key in saved:
        return "hit: " + key
    for prefix in restore_keys:
        found = [name for name in saved if name.startswith(prefix)]
        if found:
            return "partial: " + found[-1]
    return "miss"


saved = ["pip-Linux-1a2b", "pip-Windows-9f8e", "pip-Linux-3c4d"]
print(restore("pip-Linux-3c4d", ["pip-Linux-"], saved))
print(restore("pip-Linux-5e6f", ["pip-Linux-"], saved))
print(restore("pip-macOS-7a8b", ["pip-macOS-"], saved))
```

```text
hit: pip-Linux-3c4d
partial: pip-Linux-3c4d
miss
```

1. The full key exists → **hit**.
2. No full key, but the prefix matched → the newest Linux cache
   (**partial**). After a partial restore, a new cache is stored under
   the new key at the end of the job.
3. Neither → **miss**: everything is downloaded.

## Shorter: setup-python's own cache

The pip cache is so common that `actions/setup-python` can do it itself:

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
```

It makes the key from the hash of `requirements.txt` itself. If the
dependencies are in another file, it is pointed to with
`cache-dependency-path`. In simple projects a separate `actions/cache`
step is no longer needed.

## The limits of the cache

- A repository's caches are **10 GB** in total by default. When full, the
  ones unused the longest are deleted; a cache not used for 7 days is
  deleted too.
- A cache is **tied to a branch**: a cache stored on a branch is used by
  that branch and the default branch (`main`); a pull request can also
  read the cache of the branch it will be merged into. Sibling branches
  do not see each other's.
- **Do not put secrets in the cache**: it can be read from pull requests.
- A cache is a speed-up, not a guarantee. The job must work correctly
  with an empty cache too.

## Cancelling old runs

You pushed three commits to a branch in a row. Three runs start; but
only the last one's result matters. **concurrency** lets only one run in
the same group go on; `cancel-in-progress: true` cancels the old one when
a new one comes:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

The group name is the workflow + the branch: different branches do not
cancel each other. Let us see how much it saves with a model: each run
takes 10 minutes, the pushes are at minutes 0, 3 and 5.

```python
def machine_minutes(pushes, duration, cancel):
    total = 0
    for i, start in enumerate(pushes):
        end = start + duration
        if cancel and i + 1 < len(pushes):
            end = min(end, pushes[i + 1])
        total += end - start
    return total


pushes = [0, 3, 5]
print("without cancel:", machine_minutes(pushes, 10, False), "min")
print("with cancel:   ", machine_minutes(pushes, 10, True), "min")
```

```text
without cancel: 30 min
with cancel:    15 min
```

The result comes at the same time (minute 15), but 15 machine minutes are
spent instead of 30. In deployment workflows `cancel-in-progress` is used
carefully: a deployment cut in half can leave the system half done; there
the group is still written but cancelling stays off: a new run does not
start before the running one ends, and at most one run waits in the
group.

## The time limit

By default a job can run for 360 minutes (6 hours). A test stuck in an
endless loop keeps a machine busy that long. The `timeout-minutes` from
the third section puts a realistic limit on the job; for a test job that
normally takes 5 minutes, 15 minutes is enough margin.

## Other speed-ups

What we saw in the earlier sections is about speed too:

- **The path filter** (the fourth section): not running at all for a
  documentation change.
- **Parallel jobs and the critical path** (the fifth section): running
  independent jobs at the same time, starting the speed-up with the
  critical path.
- **Trimming the matrix** (the sixth section): not every combination is
  needed.
- **The quick one first:** `pytest -x` stops at the first failing test;
  for a broken PR you do not have to wait for all the tests.

Do not speed up without measuring: GitHub shows each step's duration in
its log. Look at the longest step first; most of the time that is the
dependency installation.

## All together

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            pip-${{ runner.os }}-
      - run: pip install -r requirements.txt
      - run: python -m pytest -x
```

## Summary

- Each job starts on a clean machine; the most expensive repeated work
  is installing the dependencies.
- `actions/cache`: stores and restores the `path` folder under `key`. It
  comes before the installation.
- The key is made from the content: `hashFiles('requirements.txt')`; the
  operating system is in the key too.
- `restore-keys`: if there is no full key, the newest cache starting
  with the prefix.
- `cache: pip` in `setup-python` does the same job briefly.
- `concurrency` + `cancel-in-progress` cancels old runs (careful with
  deployments). `timeout-minutes` stops a stuck job.
