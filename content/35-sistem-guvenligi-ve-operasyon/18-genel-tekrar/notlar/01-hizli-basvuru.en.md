## Program and system

| Topic | Keep in mind |
|---|---|
| Memory | Measure before writing; protections (ASLR, DEP, canaries) do not fix the bug |
| Operating system | Standard account, process isolation, default deny, hardening |
| File permissions | `644` files, `755` programs, `600` secrets; a world-writable file is a finding |
| Privilege escalation | Ownership on every request; an allow list for fields from the client |

## Software

| Topic | Keep in mind |
|---|---|
| Secure development | Shift left; fail securely; secure defaults |
| Code review | `ast.parse` reads code without running it; tools check patterns, people check meaning |
| Dependencies | Pinned versions, comparing with advisories, hashes in the lock file |
| Secrets | Not written in code or the repository; rotated first when leaked |

## Operations

| Topic | Keep in mind |
|---|---|
| Logging | Structured, UTC, no secrets and no personal data |
| Detection | Signatures find the known, anomalies the new; precision and recall |
| Incident response | Preparation, detection, containment, eradication, recovery, lessons |
| Digital forensics | Take the hash first; chain of custody; order of volatility |
| Backup | 3-2-1; RPO is data loss, RTO is downtime; test the restore |
| Cloud | Shared responsibility; default deny in IAM, deny wins |

## People and rules

| Topic | Keep in mind |
|---|---|
| Privacy | Purpose, least data, pseudonyms (HMAC), k-anonymity, retention periods |
| Ethics and law | Written permission, scope, time window; not legal advice |
| Responsible disclosure | Stop, report privately, announce together with the fix |

## Python patterns

- Constant-time comparison: `hmac.compare_digest(a, b)`.
- A file hash: `hashlib.sha256(data).hexdigest()`.
- A keyed hash: `hmac.new(key, value, hashlib.sha256).hexdigest()`.
- Secure randomness: `secrets.token_urlsafe(32)`.
- Converting to UTC: `datetime.fromisoformat(s).astimezone(timezone.utc)`.
- Counting: `Counter(...)`, threshold: `[k for k, n in c.items() if n >= limit]`.
- Inside a network: `ipaddress.ip_address(a) in ipaddress.ip_network(cidr)`.
- Reading code without running it: `ast.walk(ast.parse(source))`.
