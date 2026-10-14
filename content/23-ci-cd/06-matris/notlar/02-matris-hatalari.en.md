| Written | Result | Correct |
|---|---|---|
| `python-version: [3.10, 3.11]` | `3.10` becomes a number, `3.1` is requested | `["3.10", "3.11"]` |
| `runs-on: ubuntu-latest` (with an `os` dimension) | Every job on Linux; the `os` dimension only changes the name | `runs-on: ${{ matrix.os }}` |
| A fixed version for `setup-python` | All jobs with the same Python | `python-version: ${{ matrix.python-version }}` |
| `matrix` directly under the job | The file is invalid: `matrix` is not a job key | `strategy:` → `matrix:` |
| An `include` entry with a different original value (`python-version: "3.14"`) | It does not change an existing job, it opens a new one | Write it on purpose: a new job or an extra key? |
| `continue-on-error: true` everywhere | No failure stops the pipeline | `${{ matrix.experimental == true }}` |
| Jobs cancelled before you see where the mistake is | `fail-fast` is `true` by default | `fail-fast: false` |

**Reading which job failed**

The job name shows the combination:

```text
test (ubuntu-latest, 3.12)    ✓
test (ubuntu-latest, 3.13)    ✓
test (windows-latest, 3.13)   ✕
```

If only Windows failed, suspect: `/` and `\` in file paths, line endings
(`\r\n`), letter case (on Windows `Data.csv` and `data.csv` are the same
file), the shell difference (PowerShell).

If only the new Python failed: a feature that was removed or changed, a
dependency that is not out for that version yet.
