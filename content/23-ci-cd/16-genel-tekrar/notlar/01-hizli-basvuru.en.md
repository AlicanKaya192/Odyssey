**The file's skeleton**

```yaml
name: CI

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest -q
```

**Keys**

| Level | Key | What it does |
|---|---|---|
| Top | `on` | On which events (`push`, `pull_request`, `schedule`, `workflow_dispatch`, `merge_group`) |
| Top | `permissions` | The `GITHUB_TOKEN`'s rights |
| Top | `concurrency` | Cancels the old run in the same group |
| Job | `needs` | Order; skipped if a needed job fails |
| Job | `if` | A condition (`github.ref`, `github.event_name`) |
| Job | `strategy.matrix` | Copies; `fail-fast`, `include`, `exclude` |
| Job | `environment` | Approval, environment secrets |
| Job | `services` / `container` | Containers next to it / running inside one |
| Job | `continue-on-error` | The run does not turn red even if it fails |
| Step | `uses` + `with` | An action |
| Step | `run` (several lines with <code>&#124;</code>) | A shell command |
| Step | `env` | Environment variables for this step only |

**Expressions**

| Expression | Meaning |
|---|---|
| `${{ secrets.NAME }}` | A secret |
| `${{ vars.NAME }}` | A setting that is not secret |
| `${{ matrix.python }}` | A matrix value |
| `${{ needs.build.outputs.version }}` | Another job's output |
| `success()` / `failure()` / `always()` | The state of earlier steps and jobs |
| `startsWith(github.ref, 'refs/tags/v')` | Is it a version tag? |
| `contains(needs.*.result, 'failure')` | Did one of the needed jobs fail? |

**Common actions**

| Action | Job |
|---|---|
| `actions/checkout@v4` | Get the code |
| `actions/setup-python@v5` | Set up Python (`cache: pip`) |
| `actions/cache@v4` | Keep a folder |
| `actions/upload-artifact@v4` / `download-artifact@v4` | Move a file between jobs |
| `docker/build-push-action@v6` | Build and send an image |

**Ten rules**

1. The fast gate first.
2. Read permission at the top, write only in the job that needs it.
3. Text from outside goes through `env:`.
4. Secrets are not printed.
5. Build once; tested = released.
6. Every job has a time limit.
7. Deployments are not cancelled.
8. One required check: the gate job.
9. A flaky test is fixed, not re-run.
10. A released tag is not moved.
