## What to log, what not to log

| Log | Do not log |
|---|---|
| Login attempts (successful and failed) | Passwords, session tokens |
| Privilege changes, new accounts | Card numbers, ID numbers |
| Refused requests, authorization errors | More personal data than needed |
| Admin operations, configuration changes | A request's whole body |
| Application errors | Configuration holding secrets |

## Log levels

| Level | When? |
|---|---|
| `DEBUG` | Development detail; usually off in production |
| `INFO` | An ordinary event: a login, an operation done |
| `WARNING` | Attention: a failed login, an unexpected but harmless situation |
| `ERROR` | An operation failed |
| `CRITICAL` | A serious situation for the system or for security |

## Python patterns

- Reading a JSON line: `json.loads(line)`; `json.JSONDecodeError` on a broken line.
- Counting: `Counter(r["level"] for r in records)`.
- Converting to UTC: `datetime.fromisoformat(s).astimezone(timezone.utc)`.
- A sliding window: `deque`; drop the old: `while window[0] <= t - WINDOW: window.popleft()`.
- A hash chain: `prev = sha256((prev + entry).encode()).hexdigest()`.

## Keep in mind

- Without logs an event is neither noticed nor understood.
- A timestamp without a time zone misleads the order of events.
- Logs do not stay on the machine the attacker reached; they go to a
  separate system.
- A hash chain does not stop changes, it makes them noticeable.
- The retention period is a written decision.
