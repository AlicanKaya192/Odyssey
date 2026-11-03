# Responsible Disclosure

One day, while using a site normally, you may notice a vulnerability: an
error page shows other users' emails, or changing a number in the address
opens someone else's order. This section describes what to do at such a
moment: how to report the vulnerability to its owner **responsibly**, and
the work of the other side, the team receiving the report.

All addresses, people and vulnerability identifiers are made up. The
section builds on the permission line from the Ethics and Law section:
noticing a vulnerability and **trying it** are different things.

## When you find a vulnerability

A person holding a vulnerability has several paths:

| Path | What happens? |
|---|---|
| Staying silent | The hole stays open; someone else may find and misuse it |
| Announcing it to everyone at once (full disclosure) | Everyone learns of it before a fix is ready; users are left unprotected |
| Selling or using it | Unethical and a crime in most countries |
| **Coordinated (responsible) disclosure** | First reported privately to the owner, announced together once the fix is out |

The aim of coordinated disclosure is for the vulnerability to become public
**together with the fix**: users are protected, the owner gets a reasonable
time to fix it, and the finder gets credit for the work (thanks, sometimes
a reward).

An important limit: stop the moment you notice the vulnerability. Looking
at other records, downloading data or trying "how deep it goes" to show it
exists becomes a test done without permission.

## Whom to report to: security.txt

Many organisations write where security reports should be sent in a small
text file on their site at `/.well-known/security.txt` (RFC 9116). The file
has `Field: value` lines; `Contact` and `Expires` are required. Reading this
file is a simple text task:

```python
SECURITY_TXT = """# Security contact for shop.example.org
Contact: mailto:security@example.org
Contact: https://example.org/report
Expires: 2026-12-31T23:59:59Z
Preferred-Languages: en, tr
Policy: https://example.org/disclosure-policy
"""
fields = {}
for line in SECURITY_TXT.splitlines():
    if not line or line.startswith("#"):
        continue
    name, value = line.split(":", 1)
    fields.setdefault(name.strip().lower(), []).append(value.strip())
for name in sorted(fields):
    print(name, fields[name])
```

```text
contact ['mailto:security@example.org', 'https://example.org/report']
expires ['2026-12-31T23:59:59Z']
policy ['https://example.org/disclosure-policy']
preferred-languages ['en, tr']
```

Because a field can be written more than once (`Contact` twice), the values
were kept as a list. `split(":", 1)` splits only at the first colon;
otherwise the colon in the `https://...` address would be split too.

The `Expires` field says until when the file can be trusted; the address in
an expired file may no longer be read:

```python
from datetime import datetime, timezone

expires = datetime.fromisoformat("2026-12-31T23:59:59Z")
now = datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc)
print("expired" if expires < now else "valid")
print((expires - now).days, "days left")
```

```text
valid
58 days left
```

If there is no file, look for the site's contact page, a security team
address or the organisation's disclosure policy. A vulnerability is not
reported on **social media** or in a public bug tracker.

## A good report

The report should let the team **understand and verify** the vulnerability
quickly:

| Part | Content |
|---|---|
| Title | One sentence: what, where |
| Affected place | Address, version, page |
| How it was noticed | What you saw, and the least information needed to see it again |
| Impact | Whose data is at risk; as far as you measured |
| Suggestion | A possible fix, if you know one |
| Contact | How to reach you |

Other people's data does not go into the report; where needed it is masked
as in the Ethics and Law section. The report contains no threat or
bargaining ("pay or I publish" is blackmail).

## Time: the disclosure timeline

In coordinated disclosure, a **deadline** is usually set; a common value is
**90 days** from the report. If the fix comes out earlier, it is announced
together after a short wait so users can update. Whichever comes first:

```python
from datetime import date, timedelta

reported = date(2026, 11, 3)
deadline = reported + timedelta(days=90)
fixed = date(2027, 1, 10)
publish = min(deadline, fixed + timedelta(days=14))
print("deadline", deadline)
print("publish", publish)
```

```text
deadline 2027-02-01
publish 2027-01-24
```

Because the fix came out on 10 January, the announcement can be made two
weeks later without waiting for the deadline. The periods are not a rule
but an agreement between the two sides; for a complex vulnerability they
can be extended.

## CVE and severity

Announced vulnerabilities are usually given a **CVE** identifier: a name
in the form `CVE-year-number` that lets everyone be sure they are talking
about the same vulnerability. Its severity is often described with a
**CVSS** score (0–10), and the score is turned into a rating name:

```python
import re


def rating(score):
    if score == 0:
        return "none"
    if score < 4:
        return "low"
    if score < 7:
        return "medium"
    if score < 9:
        return "high"
    return "critical"


for cve, score in [("CVE-2099-12345", 9.8), ("CVE-2099-0042", 5.3), ("CVE-99-1", 7.5)]:
    valid = re.fullmatch(r"CVE-[0-9]{4}-[0-9]{4,}", cve) is not None
    print(cve, valid, rating(score))
```

```text
CVE-2099-12345 True critical
CVE-2099-0042 True medium
CVE-99-1 False high
```

The identifiers are made up (hence the year 2099). The third identifier
does not fit the format: the year must have four digits and the sequence
number at least four. The rating is a starting point; a vulnerability's
real risk in your system also depends on how that system is used.

## Bounty programmes and safe harbour

Some organisations run a **bug bounty programme**: they write which systems
may be tested, what is forbidden and what is paid for findings. The
programme's rules are a **permission document** and cover only the scope
they write. Many policies include a **safe harbour** clause saying that no
legal action will be taken against a good-faith researcher who follows the
rules. On a system with no programme, that assurance does not exist.

## The other side: receiving a report

There are good practices for the team receiving a report too: saying
quickly that the report was received, verifying the vulnerability, sharing
the fix timeline and thanking the finder. Whether the acknowledgement is
late can be tracked simply:

```python
from datetime import date

REPORTS = [["R-1", "2026-10-20", "2026-10-21"],
           ["R-2", "2026-10-25", None],
           ["R-3", "2026-11-01", None]]
TODAY = date(2026, 11, 3)
for rid, received, acknowledged in REPORTS:
    start = date.fromisoformat(received)
    end = date.fromisoformat(acknowledged) if acknowledged else TODAY
    days = (end - start).days
    print(rid, days, "late" if days > 5 else "ok")
```

```text
R-1 1 ok
R-2 9 late
R-3 2 ok
```

For a report not yet answered, the time is counted up to today; `R-2` has
been waiting nine days. A report left unanswered pushes the finder towards
full disclosure.

## Summary

- When you notice a vulnerability, **stop**; trying more becomes a test
  without permission.
- **Coordinated disclosure**: report privately to the owner first,
  announce together with the fix.
- Where to report is often written in the **security.txt** file; `Contact`
  and `Expires` are required.
- A good report is short, verifiable and contains no one else's data; it
  contains no blackmail.
- A **90-day** deadline is usually set for disclosure; if the fix comes out
  first, it is announced earlier.
- **CVE** is a vulnerability's shared name, **CVSS** its severity.
- A bounty programme's rules are a permission and cover only the scope
  they write.
