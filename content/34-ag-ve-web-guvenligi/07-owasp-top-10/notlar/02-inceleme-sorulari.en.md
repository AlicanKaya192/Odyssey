In code review (the Code Review and Static Analysis section), it helps to
turn the Top 10 into a list of questions. For each change, only the
questions of the categories it touches are asked.

## Access control (A01)

- Does this endpoint check who may call it?
- If a record is read with a number from the address or the body, is the
  record's owner checked?
- Do forbidden and missing give the same answer?

## Injection (A03)

- Does a value from the user enter SQL, a command or HTML by being joined
  into the text? If so, is there a parameterised query or output encoding?

## Configuration (A05)

- If a new setting was added, is its default secure?
- Are debugging, sample accounts or test endpoints going live?

## Components (A06)

- If a new library was added, is it really needed, is it still maintained,
  is its version pinned?

## Authentication (A07)

- Is there a rate limit on login, password reset and the MFA flow?
- Is the session ID renewed at login?

## Integrity (A08)

- Is anything downloaded or received from outside run or used without being
  verified?

## Logging (A09)

- Are security events (failed logins, permission errors) logged?
- Do passwords, tokens, session IDs or personal data go into the logs?

## Design (A04)

- What happens if this feature is abused? Can it be repeated without limit?
- Is there an assumption of the "nobody would try this" kind?

## An example review note

| Line | Category | Note |
|---|---|---|
| `query = "... WHERE id = " + item_id` | A03 | Turn into a parameterised query |
| `return orders[order_id]` | A01 | No ownership check |
| `log.info(f"login {user} {password}")` | A09 | The password goes into the log |
| `DEBUG = True` | A05 | Must be off in production |
