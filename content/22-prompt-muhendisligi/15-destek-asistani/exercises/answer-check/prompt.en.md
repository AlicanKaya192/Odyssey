`answer_problems(text, facts)` should list the problems in the answer in
order: `"date"` for every date in the answer (`\d{4}-\d{2}-\d{2}`) that
differs from `facts["date"]`; `"promise"` if the given `PROMISE` pattern is
found; `"action"` if the given `ACTION` pattern is found.

**Expected output:**

```
[]
['date', 'promise']
['action']
```
