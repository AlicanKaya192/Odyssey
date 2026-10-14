`build_system(settings)` should join the lines with `"\n"` and return
them: first `role`, then `tone`; if the `rules` key is there and not
empty, then a `Rules:` line and numbered lines such as `1. rule`,
`2. rule` for each rule. Without rules the `Rules:` line is not written
either.

**Expected output:**

```
You help hikers.
Be brief.
Rules:
1. No promises.
2. Be polite.
---
You help hikers.
Be brief.
```
