**Four strategies**

| Strategy | Downtime | Two versions at once | Rollback speed | Extra resources |
|---|---|---|---|---|
| Recreate | Yes | No | Slow | None |
| Rolling | No | Yes | Medium | None (capacity drops) |
| Blue-green | No | A short moment | Instant | Two full copies |
| Canary | No | Yes | Fast | Little |

**When to use which?**

- If downtime is acceptable (night maintenance, an internal tool):
  recreate.
- Many servers, no extra resources: rolling.
- Instant rollback is a must: blue-green.
- A risky change, many users: canary.

**The canary decision**

| Situation | Decision |
|---|---|
| Not enough requests | Wait |
| New error rate > old one + allowed increase | Pull back |
| Otherwise | Raise the share |

```python
def decide(old, new, max_increase=0.01, min_requests=500):
    if new[1] < min_requests:
        return "wait"
    if new[0] / new[1] > old[0] / old[1] + max_increase:
        return "rollback"
    return "promote"
```

**Rolling back**

- Deploy **the same package** of the previous version again; do not
  revert the code and build again.
- Packages are kept with their version number.
- Database: expand first, contract later; this way you can always go back
  one version.
- In rolling and canary deployments two versions run side by side: the
  new version must not write a data format the old one cannot understand.
