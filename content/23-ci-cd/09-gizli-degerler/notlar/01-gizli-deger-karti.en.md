**What lives where?**

| What | Where | In the workflow | In the log |
|---|---|---|---|
| Password, API key | Settings › Secrets and variables › Actions › Secrets | `${{ secrets.NAME }}` | `***` (exact value) |
| Setting that is not secret | Same page › Variables | `${{ vars.NAME }}` | Open |
| The run's temporary key | GitHub gives it by itself | `${{ secrets.GITHUB_TOKEN }}` | `***` |

**Using a secret**

```yaml
      - run: python send_report.py
        env:
          REPORT_API_KEY: ${{ secrets.REPORT_API_KEY }}
```

```python
import os

key = os.environ["REPORT_API_KEY"]
```

**Name rules**

- Letters, digits, underscores. No spaces.
- Does not start with a digit; does not start with `GITHUB_`.
- Once saved, the value is not shown on the page; it can only be changed.

**What masking does and does not do**

| Case | In the log |
|---|---|
| The value was printed exactly | `***` |
| The value was turned into base64, JSON or another form | Shown openly |
| Part of the value was printed | Shown openly |
| The derived value was added with `::add-mask::` | `***` |

```yaml
      - run: echo "::add-mask::$DERIVED"
```

**When does it not come?**

- In a PR opened from a fork, secrets come in empty (`GITHUB_TOKEN` comes
  only with read access).
- Steps that need secrets run on a push to `main` or when a tag arrives,
  not in a PR.

**If a key leaked**

1. **Revoke** the old key at the service.
2. Get a new key, write it into the store.
3. Deleting the line alone is not enough: git history keeps it.
