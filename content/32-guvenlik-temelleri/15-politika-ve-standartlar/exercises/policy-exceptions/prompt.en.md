Each exception is a dictionary with the fields `id`, `owner`, `expires`
(`"YYYY-MM-DD"`) and `compensating`; some fields are empty or missing.

`policy_exceptions(exceptions, today)` should return the problems as
`"<id>: <problem>"`. Exceptions in `id` order, and within each exception
the problems in this order:

1. `owner` empty or missing → `"no owner"`
2. `expires` empty or missing → `"no end date"`; if present and before
   `today` → `"expired"` (one ending today is still valid)
3. `compensating` empty or missing → `"no compensating control"`

Dates in this format can be compared as text.

**Expected output:**

```
EX-1: no owner
EX-1: no compensating control
EX-3: expired
EX-4: no end date
```
