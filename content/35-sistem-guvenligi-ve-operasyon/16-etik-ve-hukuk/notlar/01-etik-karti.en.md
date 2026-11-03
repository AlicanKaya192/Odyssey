## Concepts

| Concept | Meaning |
|---|---|
| Written permission | The system owner approving the test in writing |
| Rules of engagement | The document stating the test's scope, timing and limits |
| Scope | The addresses and systems permitted |
| Excluded | A system not tested even though it is inside the scope |
| Time window | The days and hours when the test may run |
| Dual-use knowledge | Knowledge usable both in defence and in attack |
| Conflict of interest | Another tie that may affect impartiality |

## Before starting a test

- Is there written permission, and is the person giving it the system's
  owner?
- Is the scope written address by address, and are exclusions clear?
- Are the time window and the time zone set?
- Whom do we call in an emergency?
- How will the data seen be stored, and when deleted?
- If the system is on a cloud service, have the provider's testing rules
  been read?

## Python patterns

- Missing field: `[n for n in required if not plan.get(n)]`.
- Inside a network: `ipaddress.ip_address(a) in ipaddress.ip_network(cidr)`.
- Date range: `start <= day <= end`.
- Masking an email: `user[0] + "***@" + domain`.

## Keep in mind

- Good intentions do not replace permission.
- Permission is given to what is written; "it is the same network anyway"
  is not scope.
- Having access does not mean being able to give permission.
- Showing a vulnerability does not require downloading all the data.
- This card is not legal advice; for details, consult the law itself and a
  lawyer.
