# Versioning and Tags

In the eighth section we built the package, in the ninth we saw how to
keep keys safe and narrow down permissions. One last step is left:
**releasing the package with a version number**. Users read the answers to
"which version am I on, what changed in the new one, will something break
if I update?" from the version number. In this section we see how to pick
the number, how to mark it in git and how that mark starts the pipeline.

## Semantic versioning

The most common rule is **semantic versioning** (SemVer for short). The
number has three parts: `MAJOR.MINOR.PATCH`, for example `2.4.1`.

<figure class="fig anat">
  <div class="anat-row"><span><code>MAJOR</code></span><span>A change that is not compatible with the old one: someone using the old code may find their code broken after updating. <code>1.9.3</code> → <code>2.0.0</code></span></div>
  <div class="anat-row"><span><code>MINOR</code></span><span>A backward compatible new feature. <code>1.9.3</code> → <code>1.10.0</code></span></div>
  <div class="anat-row"><span><code>PATCH</code></span><span>Only a bug fix. <code>1.9.3</code> → <code>1.9.4</code></span></div>
</figure>

When a part goes up, the ones to its right are reset: the release with a
new feature after `1.9.3` is `1.10.0`, not `1.10.3`. `0.x` versions mean
"not stable yet"; anything may change there.

## Versions do not sort like text

`1.10.0` is newer than `1.9.0`. But comparing versions as text finds the
opposite, because texts are compared character by character and `"1"` is
smaller than `"9"`:

```python
versions = ["1.9.0", "1.10.0", "1.2.3", "0.9.12"]
print(sorted(versions))


def as_tuple(version):
    return tuple(int(part) for part in version.split("."))


print(sorted(versions, key=as_tuple))
print("1.10.0" > "1.9.0", as_tuple("1.10.0") > as_tuple("1.9.0"))
```

```text
['0.9.12', '1.10.0', '1.2.3', '1.9.0']
['0.9.12', '1.2.3', '1.9.0', '1.10.0']
False True
```

Turning the parts into numbers and comparing them as a **tuple** gives the
right order: tuples are also compared from left to right, but every part
is a number, `10 > 9`.

Python package numbers know a little more than SemVer (PEP 440): trial
versions before a release are `1.2.0b2` (beta) and `1.2.0rc1` (release
candidate), and a small fix after a release is `1.2.0.post1`. Sorting
these by hand is hard; the `packaging` library (the one pip itself uses)
knows the right order:

```python
from packaging.version import Version

candidates = ["1.2.0", "1.2.0rc1", "1.2.0b2", "1.1.9", "1.2.0.post1"]
for version in sorted(candidates, key=Version):
    print(version)
```

```text
1.1.9
1.2.0b2
1.2.0rc1
1.2.0
1.2.0.post1
```

A candidate comes **before** the real release: `1.2.0rc1 < 1.2.0`. That
is why pip does not install candidates by itself; it installs them when
asked with `--pre`.

## Which part goes up?

Picking the number by hand invites forgetting. A common solution is
writing a prefix in commit messages (**Conventional Commits**):

| Prefix | Meaning | Version |
|---|---|---|
| `fix: ...` | Bug fix | PATCH |
| `feat: ...` | New feature | MINOR |
| `feat!: ...` or `BREAKING CHANGE` in the text | Incompatible change | MAJOR |
| `docs: ...`, `test: ...`, `ci: ...` | Nothing the user sees changed | No new version |

The largest of the commits since the last release wins: with one `feat`
and three `fix`es, MINOR goes up. Raising the number is a small function:

```python
def bump(version, part):
    major, minor, patch = (int(p) for p in version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


print(bump("1.9.3", "patch"))
print(bump("1.9.3", "minor"))
print(bump("1.9.3", "major"))
```

```text
1.9.4
1.10.0
2.0.0
```

The part that reads the prefixes and decides which part goes up is in the
exercises. There are ready-made tools that produce the version number and
the release notes by this rule (e.g. `release-please`,
`semantic-release`); all of them are built on this table.

## A tag: a permanent name for a commit

In git a version is marked with a **tag**: a name given to a particular
commit that does not move on like a branch. Whatever code a released
version came from, the tag points at it.

```text
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

- `-a` is an annotated tag: it also keeps who added it, when, and with
  which message. This is the one recommended for releases.
- Tags are not sent by `git push` by themselves; they are sent by name.
- The name usually starts with `v`: `v1.2.0`. The package's own number is
  written without the `v` in `pyproject.toml`: `1.2.0`.
- **A published tag is not moved.** Pointing `v1.2.0` at another commit
  means that everyone who downloaded it has something different from the
  repository. If there was a bug, release a new version: `v1.2.1`.

As we saw in the fourth section, sending a tag is a `push` event and is
caught with the `tags` filter. Inside a run the tag's name is in the
`GITHUB_REF_NAME` environment variable (`${{ github.ref_name }}` in the
workflow).

## The tag and the package should say the same number

A common mistake: the tag is `v1.2.0`, but `pyproject.toml` still says
`version = "1.1.0"`. The released package calls itself `1.1.0` and pip
thinks it is an old version. The pipeline should check this before
building:

```python
import tomllib

PYPROJECT = '[project]\nname = "greeter"\nversion = "0.2.0"\n'


def check_tag(tag, pyproject_text):
    version = tomllib.loads(pyproject_text)["project"]["version"]
    if tag != "v" + version:
        return f"tag {tag} does not match version {version}"
    return "ok"


print(check_tag("v0.2.0", PYPROJECT))
print(check_tag("v0.2.1", PYPROJECT))
```

```text
ok
tag v0.2.1 does not match version 0.2.0
```

In the pipeline it is a small script: it reads `pyproject.toml`, compares
it with the tag and, if they do not match, ends with a non-zero exit code;
the job fails there and a package with the wrong number is not released.

## The release pipeline

All together: when a tag arrives, test, check the number, build and
create a GitHub release.

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: python -m pytest
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python scripts/check_version.py "$GITHUB_REF_NAME"
      - run: python -m pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  release:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
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

- Only tags starting with `v` start the pipeline; a push to `main` does
  not.
- The package is built once (`build`); the `release` job downloads the
  same files (eighth section).
- The `release` job did not get the code; `gh` learns which repository to
  work on from `--repo`. `GITHUB_REPOSITORY` holds the name as
  `owner/repo`.
- `--generate-notes` has GitHub itself write the release notes from the
  PRs merged since the last release.
- Write permission only in the `release` job (ninth section).

## Uploading to the package index (PyPI)

For the package to be installable with `pip install greeter`, it is
uploaded to **PyPI**. It used to take a permanent PyPI key kept as a
secret. Today the recommended way is **trusted publishing**: on PyPI you
state once that "this workflow of this repository may upload"; on every
run the job gets a short-lived identity (`id-token`) from GitHub and
uploads with it. There is no key to keep or to leak.

```yaml
  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - uses: pypa/gh-action-pypi-publish@release/v1
```

- `environment: pypi` ties the job to an **environment** on GitHub; rules
  like "ask for approval before uploading" can be set on an environment
  (eleventh section).
- `id-token: write` is the only permission needed to get the short-lived
  identity.
- A version number uploaded to PyPI **can never be used again**, even if
  it is deleted. There is a separate test index (TestPyPI) for trials.

## Next

We released the package. In the eleventh section we look at ways of
deploying an application to a server: environments, approval steps and
going back if something goes wrong.

## Summary

- Semantic versioning: `MAJOR.MINOR.PATCH`; an incompatible change is
  MAJOR, a new feature MINOR, a fix PATCH. The parts to the right of the
  one that goes up are reset.
- Versions do not sort as text (`"1.10.0" < "1.9.0"`); they are turned
  into numbers and compared. In Python `packaging.version.Version` also
  knows the `rc`, `b` and `post` suffixes.
- Commit prefixes (`fix:`, `feat:`, `feat!:`) say which part the next
  version raises.
- A version is marked with an annotated tag and sent by name; a published
  tag is not moved.
- The pipeline starts with a tag (`tags: ["v*"]`), checks that the tag
  says the same number as `pyproject.toml`, builds once and releases.
- To upload to PyPI without a key: trusted publishing and
  `id-token: write`.
