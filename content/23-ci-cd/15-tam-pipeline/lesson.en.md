# Capstone: A Full Pipeline for a Python Project

In this module we built the pieces of the pipeline one by one: tests,
quality gates, triggers, jobs, the matrix, caching, packages, secrets,
versions, deployment, branch rules. In this section we put them all
together in **one pipeline for one project**. The goal is less about
learning something new and more about being able to say why each piece
is there.

## The project

A small Python package that converts temperatures: `tempconv`.

```text
tempconv-project/
├── .github/workflows/ci.yml
├── pyproject.toml
├── requirements-dev.txt
├── scripts/check_version.py
├── tempconv/
│   ├── __init__.py
│   └── convert.py
└── tests/
    └── test_convert.py
```

```python
def c_to_f(celsius):
    return round(celsius * 9 / 5 + 32, 2)


def f_to_c(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 2)
```

```python
import pytest

from tempconv.convert import c_to_f, f_to_c

CASES = [(0, 32), (100, 212), (-40, -40), (37, 98.6)]


@pytest.mark.parametrize("celsius, fahrenheit", CASES)
def test_c_to_f(celsius, fahrenheit):
    assert c_to_f(celsius) == fahrenheit


def test_round_trip():
    assert f_to_c(c_to_f(21.5)) == 21.5
```

The tests in the project folder:

```text
> python -m pytest -q
.....                                                                    [100%]
5 passed
```

`requirements-dev.txt` lists the development tools
(`pytest`, `pytest-cov`); `scripts/check_version.py` is the script from
the tenth section: is the tag the same as the version in
`pyproject.toml`?

## The pipeline's contract

Before the YAML, let's write down what the pipeline will **guarantee**.
There is a section behind every row:

| Guarantee | How | Section |
|---|---|---|
| Every PR and `main` is tested | `push` + `pull_request` + `merge_group` | 4, 13 |
| No format or lint errors get in | `ruff check`, `ruff format --check` | 2 |
| Tests pass on two Python versions | Matrix, `fail-fast: false` | 1, 6 |
| Tests touch at least 90% of the code | `--cov-fail-under=90` | 2 |
| The package is built once | `build` + artifact | 8 |
| One name for the required check | The `ci-ok` gate job | 13 |
| Release only on a `v` tag, version consistent | `if:` + `check_version.py` | 10 |
| Least permission | `contents: read` at the top, `write` in the release | 9 |
| No wasted runs, no hanging jobs | `concurrency`, `timeout-minutes`, `cache` | 7 |

## 1. Triggers and general settings

```yaml
name: CI

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]
  merge_group:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
```

In the seventh section we wrote `cancel-in-progress: true`. Here we
cancel only in PRs: when a new commit comes to a PR the old run is
wasted, but every run of `main` and of a tag must finish (each one is the
record of a version).

## 2. Lint and tests

```yaml
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install ruff
      - run: python -m ruff check .
      - run: python -m ruff format --check .
  test:
    needs: lint
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
      - run: python -m pip install -r requirements-dev.txt
      - run: python -m pytest -q --cov=tempconv --cov-fail-under=90
```

- Lint first: if the gate that takes seconds fails, the tests that take
  minutes never start ("the fast gate first" from the second section).
- `fail-fast: false`: a test that fails on one version should not hide
  the other version's result.
- `cache: pip` does not download the packages again on every run.

## 3. The package and the gate

```yaml
  build:
    needs: test
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
  ci-ok:
    if: always()
    needs: [lint, test, build]
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
        if: >-
          contains(needs.*.result, 'failure')
          || contains(needs.*.result, 'cancelled')
      - run: echo "all checks passed"
```

The package is built on every run: in PRs too. This way a "the package
does not build" error is not left for release day. In the branch rule for
`main`, only `ci-ok` is written as the required check.

## 4. The release

```yaml
  release:
    needs: ci-ok
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/check_version.py "$GITHUB_REF_NAME"
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: |
          gh release create "$GITHUB_REF_NAME" dist/* \
            --repo "$GITHUB_REPOSITORY" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- `needs: ci-ok`: the release is behind the gate. The gate runs with
  `if: always()`, but if it fails the release is skipped.
- Write permission only in this job; the default at the top of the file
  is read.
- The released files are the same package `build` built and that was
  tested.

The four pieces one under another make one file:
`.github/workflows/ci.yml`.

## How long does the pipeline take?

The critical path from the fifth section: a job starts when the latest
job it depends on finishes. Let's estimate the minutes and compute (the
two copies of the matrix run at the same time, so `test` is one row):

```python
jobs = {
    "lint": (1, []),
    "test": (4, ["lint"]),
    "build": (1, ["test"]),
    "ci-ok": (0, ["lint", "test", "build"]),
    "release": (1, ["ci-ok"]),
}


def finish(name):
    minutes, needs = jobs[name]
    return minutes + max((finish(n) for n in needs), default=0)


for name in jobs:
    print(f"{name:<8} done at minute {finish(name)}")

jobs["test"] = (4, [])
print("test without lint first:", finish("release"))
```

```text
lint     done at minute 1
test     done at minute 5
build    done at minute 6
ci-ok    done at minute 6
release  done at minute 7
test without lint first: 6
```

Putting lint before the tests makes a green release one minute longer; in
return, in a PR with a format error the two test machines never start.
This is a choice: if the pipeline is slow and lint rarely fails, the two
can also run in parallel. What matters is making the choice knowingly.

## Repository settings

The pipeline's file is not enough; three more settings on GitHub:

- **Settings › Rules:** for `main`, a PR required, at least one approval,
  the required check `ci-ok`, force pushes blocked.
- **Settings › Actions › General:** workflow permissions "read only" by
  default.
- **A tag rule:** only maintainers can create `v*` tags; otherwise anyone
  who can push a tag makes a release.

## Final checklist

- When a PR is opened, do lint, two tests, the package and `ci-ok` run?
- In a PR that only changes `README.md`, does `ci-ok` still report a
  result? (This pipeline has no path filter, so it does. If a filter is
  added, the trap from the thirteenth section comes back.)
- When you break a test on purpose, is `ci-ok` red and merging closed?
- With `pyproject.toml` at `0.3.0`, does a `v0.3.1` tag stop the release?
- With a `v0.3.0` tag, are the `dist` files on the release page?

## Next

The sixteenth section is the overall review: we test the whole module
with questions and mixed exercises.

## Summary

- The contract first, then the YAML: every guarantee rests on a piece,
  every piece on a section.
- The triggers are `push`, `pull_request`, `merge_group` and the `v*`
  tag; cancelling only in PRs.
- Lint first, tests with a matrix and a coverage threshold, the package
  once, one required check `ci-ok`.
- The release only on a tag, behind the gate, with a version check and
  its own write permission.
- The critical path gives the pipeline's duration; the order is a choice
  of speed and cost.
- Branch rules and permission settings matter as much as the pipeline's
  file.
