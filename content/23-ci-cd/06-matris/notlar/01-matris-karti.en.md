**Layout**

```yaml
  test:
    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.experimental == true }}
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.13"]
        exclude:
          - os: windows-latest
            python-version: "3.12"
        include:
          - os: ubuntu-latest
            python-version: "3.14"
            experimental: true
```

`strategy` is under the job (in the same column as `runs-on`), `matrix`
under `strategy`, `exclude` and `include` under `matrix`.

**Keys**

| Key | Meaning |
|---|---|
| `matrix.<dimension>` | A list of values; the number of jobs is the product of the lengths |
| `exclude` | Removes matching combinations (applied first) |
| `include` | Adds keys to a matching combination; one that does not match becomes a new job |
| `fail-fast` | `true` by default: when one fails, the others are cancelled |
| `max-parallel` | At most how many jobs at the same time |

**Reading a value**

- `${{ matrix.os }}`, `${{ matrix.python-version }}`
- A key added with `include` only to some jobs is empty in the others.

**Numbers**

| Matrix | Jobs |
|---|---|
| 2 operating systems × 2 versions | 4 |
| 3 × 4 | 12 |
| 3 × 4 × 2 (two dependency versions) | 24 |
| At most from one matrix | 256 |

**A common setup**

- All Python versions on Linux.
- Windows and macOS only with the newest version (with `include`).
- A version that is not out yet: `experimental: true` + `continue-on-error`.
