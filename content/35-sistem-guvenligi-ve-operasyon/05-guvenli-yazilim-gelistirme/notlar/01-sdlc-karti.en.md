## Security work step by step

| Step | Work | Output |
|---|---|---|
| Requirements | Security requirements | Testable sentences such as "only the owner deletes" |
| Design | A threat model, secure defaults | A threat list, defense decisions |
| Coding | Secure coding, code review | Reviewed changes |
| Verification | Security tests, static analysis, dependency scanning | Test and scan reports |
| Release and maintenance | A release gate, patching, monitoring | A release that passed the gate, incident records |

## Four principles

| Principle | In short |
|---|---|
| Fail securely | Refuse when there is an error (fail closed) |
| Secure defaults | A dangerous setting only when explicitly asked for |
| Validate input | An allow list: describe the good |
| Defense in depth | Do not trust a single check |

## Python patterns

- Catch only the expected error: `except KeyError: return False`.
- Only known keys over the defaults:
  `if key in DEFAULTS: config[key] = value`.
- Validating a number: `text.isdigit()` and the range `1 <= value <= 100`.
- A release gate: `[item for item, done in checklist.items() if not done]`.

## Keep in mind

- `except Exception: return True` are the two most dangerous lines in a
  security check.
- A security test's value is in its "must not" cases.
- A deny list gets forgotten; an allow list refuses on its own.
- A gate is not passed "just this once".
