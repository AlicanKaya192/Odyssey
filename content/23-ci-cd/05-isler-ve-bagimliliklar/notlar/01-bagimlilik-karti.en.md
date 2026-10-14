**Between jobs**

| Written | Meaning |
|---|---|
| (nothing) | Jobs at the same time, on separate machines |
| `needs: test` | Start when `test` has finished successfully |
| `needs: [lint, test]` | Start when both have finished successfully |
| `continue-on-error: true` | The run counts as successful even if this job fails |

**Status functions** (inside `if`)

| Function | When it is true |
|---|---|
| `success()` | All the previous jobs succeeded (the default) |
| `failure()` | One of the previous jobs failed (including ones further back in the chain) |
| `always()` | Always |
| `cancelled()` | The run was cancelled |

**Context values**

| Value | Example |
|---|---|
| `github.event_name` | `push`, `pull_request`, `schedule` |
| `github.ref` | `refs/heads/main`, `refs/tags/v1.2.0` |
| `github.ref_name` | `main`, `v1.2.0` |
| `github.sha` | The commit's id |
| `github.actor` | The user who started the run |
| `needs.<job>.result` | `success`, `failure`, `skipped` |
| `needs.<job>.outputs.<name>` | A value the job exposes |

**Writing conditions**

- Text in single quotes: `github.ref == 'refs/heads/main'`
- `&&` and, `||` or, `!` not
- No `${{ }}` needed inside `if`
- If there is no status function, `success() &&` is added in front

**Passing a value**

```yaml
  version:
    runs-on: ubuntu-latest
    outputs:
      number: ${{ steps.read.outputs.number }}
    steps:
      - id: read
        run: echo "number=1.4.2" >> "$GITHUB_OUTPUT"
  build:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ needs.version.outputs.number }}"
```
