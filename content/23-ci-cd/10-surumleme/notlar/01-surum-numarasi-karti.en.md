**Semantic versioning: `MAJOR.MINOR.PATCH`**

| Change | Goes up | Example (from `1.9.3`) |
|---|---|---|
| Incompatible with the old one | MAJOR | `2.0.0` |
| Backward compatible new feature | MINOR | `1.10.0` |
| Only a bug fix | PATCH | `1.9.4` |

- The parts to the right of the one that goes up are reset.
- `0.x`: not stable yet.

**Commit prefixes (Conventional Commits)**

| Prefix | Version |
|---|---|
| `fix:` | PATCH |
| `feat:` | MINOR |
| `feat!:`, `fix!:` or `BREAKING CHANGE` in the text | MAJOR |
| `docs:`, `test:`, `ci:`, `refactor:` | No new version |

The **largest** of the commits since the last release wins.

**Sorting**

```python
# Wrong: as text
sorted(["1.9.0", "1.10.0"])            # ['1.10.0', '1.9.0']

# Right: a tuple of numbers
def as_tuple(version):
    return tuple(int(part) for part in version.split("."))

sorted(["1.9.0", "1.10.0"], key=as_tuple)   # ['1.9.0', '1.10.0']
```

```python
# Python packages (PEP 440): sorting that also knows the suffixes
from packaging.version import Version

sorted(["1.2.0", "1.2.0rc1", "1.2.0b2"], key=Version)
# ['1.2.0b2', '1.2.0rc1', '1.2.0']
```

**PEP 440 suffixes**

| Form | Meaning | Order |
|---|---|---|
| `1.2.0b2` | Beta | Before `1.2.0` |
| `1.2.0rc1` | Release candidate | After beta, before `1.2.0` |
| `1.2.0` | Release | |
| `1.2.0.post1` | Small fix after the release | After `1.2.0` |

pip installs candidate and beta versions only with `--pre`.
