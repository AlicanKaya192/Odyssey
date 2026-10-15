**Triggers**

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, edited, synchronize, reopened]
  merge_group:
```

| Event | When |
|---|---|
| `pull_request` (default) | When opened, on a new commit, when reopened |
| `edited` in `types` | Also when the title or description changes |
| `merge_group` | While the PR is tested in the merge queue |
| `push` to `main` | `main` itself after a merge |

**The gate job**

```yaml
  ci-ok:
    if: always()
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
        if: >-
          contains(needs.*.result, 'failure')
          || contains(needs.*.result, 'cancelled')
      - run: echo "lint and test passed or were skipped"
```

Only `ci-ok` on the required list.

| `needs.*.result` value | The gate |
|---|---|
| All `success` | Passes |
| One `skipped` | Passes (a skipped job is fine) |
| One `failure` | Fails |
| One `cancelled` | Fails |

**The PR title check**

```yaml
  title:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/check_title.py "$TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

- The title goes through `env:`; it is not written into the `run:` line
  with `${{ }}` (code injection).
- With a squash merge, the PR title becomes the commit message.

**`pull_request` and `pull_request_target`**

| | `pull_request` | `pull_request_target` |
|---|---|---|
| Which code | The PR's merged form | The target branch's code |
| Secrets from a fork | Empty | Filled |
| `GITHUB_TOKEN` | Read | Can be write |
| For tests | Yes | Never run the PR's code |
