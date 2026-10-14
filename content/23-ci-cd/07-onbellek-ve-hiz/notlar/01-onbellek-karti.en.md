**actions/cache**

| Setting | Meaning |
|---|---|
| `path` | The folder to store (for pip, `~/.cache/pip`) |
| `key` | The full key; must change when the content changes |
| `restore-keys` | Fallback prefixes; if there is no full key, the newest match |

**Results**

| Case | What happens |
|---|---|
| hit | The full key was found; the folder is restored, not stored again at the end |
| partial | A prefix matched; the newest match is restored, stored under the new key at the end |
| miss | Neither; everything is downloaded, stored at the end |

**A good key**

```text
pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
```

- The tool's name (`pip`): so it does not mix with other caches.
- `runner.os`: so operating systems do not mix.
- `hashFiles(...)`: a new key when the dependencies change.

**The short way**

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
```

**Limits**

- 10 GB per repository by default; unused for 7 days → deleted.
- Tied to a branch: the branch + the default branch; a PR reads its
  target branch's.
- No secrets in the cache.
- The job must work correctly with an empty cache too.

**concurrency**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

| Setting | Meaning |
|---|---|
| `group` | One of the runs in the same group goes on |
| `cancel-in-progress: true` | When a new one comes, the old one is cancelled (test pipelines) |
| `cancel-in-progress: false` | The new one waits for the old one to finish (deployment) |
