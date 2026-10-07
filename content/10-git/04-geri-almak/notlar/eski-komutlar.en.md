Most solutions you find online were written before Git 2.23 (2019) and use
the old commands instead of `restore` / `switch`. They all still work; you
only need to know what they correspond to.

| Old form | New form | What it does |
|---|---|---|
| `git checkout -- file` | `git restore file` | Throw away the change in a file. |
| `git reset HEAD file` | `git restore --staged file` | Unstage. |
| `git checkout HEAD~2 -- file` | `git restore --source=HEAD~2 file` | Bring back an old version of a file. |
| `git checkout branch` | `git switch branch` | Switch to a branch (06). |
| `git checkout -b new` | `git switch -c new` | Create a branch and switch to it (06). |

## Why was it split in two?

`git checkout` did two very different jobs: switching branches and restoring
files. A one-character difference (`--`) decided which one, and someone who
typed it wrong could lose their changes. `switch` only changes branches,
`restore` only touches files.

## `reset` with a file

`git reset file` (without a commit, with a file name) also unstages, the
same as `git restore --staged file`. `--hard` cannot be used with a file
name:

```text
fatal: Cannot do hard reset with paths.
```
