## Concepts

| Concept | Meaning |
|---|---|
| Coordinated disclosure | Reporting privately to the owner first, announcing together with the fix |
| Full disclosure | Announcing a vulnerability to everyone without waiting for a fix |
| security.txt | The file stating where security reports should go (RFC 9116) |
| CVE | The shared identifier of an announced vulnerability: `CVE-year-number` |
| CVSS | A system describing a vulnerability's severity with a 0–10 score |
| Bug bounty programme | A written invitation to test, with scope and rewards |
| Safe harbour | A promise of no legal action against a good-faith researcher who follows the rules |

## CVSS ratings

| Score | Rating |
|---|---|
| 0.0 | None |
| 0.1–3.9 | Low |
| 4.0–6.9 | Medium |
| 7.0–8.9 | High |
| 9.0–10.0 | Critical |

## Before reporting

- Did I stop when I noticed the vulnerability, and look at no other record?
- Whom will I report to: security.txt, a security team address, a
  disclosure policy?
- Does the report contain no one else's data?
- Is the impact I wrote only as far as I measured?
- If there is a bounty programme, have I read its rules and scope?

## Python patterns

- Splitting at the first colon: `name, value = line.split(":", 1)`.
- A multi-valued field: `fields.setdefault(name, []).append(value)`.
- A time ending in `Z`: `datetime.fromisoformat("2026-12-31T23:59:59Z")`.
- Whichever comes first: `min(deadline, fixed + timedelta(days=14))`.
- A format check: `re.fullmatch(r"CVE-[0-9]{4}-[0-9]{4,}", s)`.

## Keep in mind

- Noticing and trying are different.
- A report goes through a private channel, not social media.
- "Pay or I publish" is not disclosure but blackmail.
- Programme rules are a permission; where there is no programme, there is
  no assurance.
