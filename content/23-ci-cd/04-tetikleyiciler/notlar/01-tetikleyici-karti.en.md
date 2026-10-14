**Events**

| Event | When |
|---|---|
| `push` | When commits are pushed to a branch or a tag |
| `pull_request` | When a PR is opened, gets new commits, is reopened |
| `schedule` | At the time in the cron expression (UTC) |
| `workflow_dispatch` | With the Run workflow button in the Actions tab |

**Filters** (under `push` and `pull_request`)

| Filter | Meaning |
|---|---|
| `branches` | Only on these branches (for a PR: the target branch) |
| `branches-ignore` | On every branch but these; not written together with `branches` |
| `tags` | When these tags are pushed (`push`) |
| `paths` | If one of these files changed |
| `paths-ignore` | Does not run if all the changed files are among these |

If the branch and path filters are together, **both conditions** must
hold.

**Patterns**

| Pattern | Matches | Does not match |
|---|---|---|
| `release/*` | `release/1.0` | `release/2026/oct` |
| `release/**` | `release/2026/oct` | `hotfix/1` |
| `*.md` | `README.md` | `docs/guide.md` |
| `**.md` | `docs/guide.md` | `docs/logo.png` |
| `docs/**` | `docs/img/logo.png` | `src/docs.py` |

`*` does not match a slash, `**` does.

**A common setup**

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

**Traps**

- An unfiltered `on: [push, pull_request]`: a push to an open PR's
  branch starts two runs.
- With only `tags`, branch pushes do not start it; with only `branches`,
  tag pushes do not start it.
- `schedule` and `workflow_dispatch` are read only from the file on the
  default branch.
- `[skip ci]` in the commit message: the runs of that push are skipped.
