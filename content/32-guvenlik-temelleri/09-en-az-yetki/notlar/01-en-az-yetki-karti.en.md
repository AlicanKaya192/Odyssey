## Terms

| Term | Meaning |
|---|---|
| **Least privilege** | Enough privilege for the job, no more |
| **Need to know** | Information is not given if the job does not need it, even if the level allows |
| **Privilege creep** | Old privileges not being taken away when roles change |
| **Access review** | Regularly asking whether every privilege is still needed |
| **Just-in-time access** | A privilege that is requested, approved and drops by itself soon after |
| **Separation of duties** | Steps that could be abused are held by different people |
| **Two-person rule** | Two people's approval for an important action |
| **Break-glass account** | An account kept in a safe that sets off an alarm when used and is reviewed afterwards |

## Python patterns

```python
extra = held - needed
unused = granted - used
has_conflict = set(pair) <= perms
active = date.fromisoformat(until) >= today
```

- `-` set difference: what is in one but not the other.
- `<=` subset for sets: are all of them in the other?
- `date.fromisoformat("2026-11-02")`: a date from text.

## Practice list

- A non-administrator account for daily work.
- Programs' database users only on the tables they need.
- When a role changes, the old role's privileges are removed **the same
  day**.
- All access of a leaver is closed **the same day**.
- An access review every three months; unused privileges are suggested
  for removal.
- Short-term needs are given with an end date.
- Conflicting duty pairs are written down and checked at every role
  assignment.
