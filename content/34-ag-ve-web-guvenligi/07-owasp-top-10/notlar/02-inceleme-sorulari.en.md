In code review (the Code Review and Static Analysis section), it helps to
turn the Top 10 into a list of questions. For each change, only the
questions of the categories it touches are asked. The numbers are from the
2025 edition.

## Access control (A01)

- Does this endpoint check who may call it?
- If a record is read with a number from the address or the body, is the
  record's owner checked?
- Do forbidden and missing give the same answer?
- If the server sends a request to an address the user gives (SSRF), is the
  target checked against an allow list?

## Configuration (A02)

- If a new setting was added, is its default secure?
- Are debugging, sample accounts or test endpoints going live?

## Supply chain (A03)

- If a new library was added, is it really needed, is it still maintained,
  is its version pinned, does it come from a trusted source?

## Injection (A05)

- Does a value from the user enter SQL, a command or HTML by being joined
  into the text? If so, is there a parameterised query or output encoding?

## Design (A06)

- What happens if this feature is abused? Can it be repeated without limit?
- Is there an assumption of the "nobody would try this" kind?

## Authentication (A07)

- Is there a rate limit on login, password reset and the MFA flow?
- Is the session ID renewed at login?

## Integrity (A08)

- Is anything downloaded or received from outside run or used without being
  verified?

## Logging and alerting (A09)

- Are security events (failed logins, permission errors) logged? Do the
  important ones alert someone?
- Do passwords, tokens, session IDs or personal data go into the logs?

## Exceptional conditions (A10)

- If an error happens inside a check, does the result become "allow"?
- Is there a broad `except` that silences every error?

## An example review note

| Line | Category | Note |
|---|---|---|
| `query = "... WHERE id = " + item_id` | A05 | Turn into a parameterised query |
| `return orders[order_id]` | A01 | No ownership check |
| `log.info(f"login {user} {password}")` | A09 | The password goes into the log |
| `DEBUG = True` | A02 | Must be off in production |
| `except Exception: return True` | A10 | Allows when an error happens |
