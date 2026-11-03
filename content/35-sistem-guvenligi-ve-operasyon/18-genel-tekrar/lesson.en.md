# Overall Review

This module took security from inside a program all the way to how an
organisation runs: how memory gets corrupted and how it is protected, the
operating system's permissions, secure software development, secrets and
dependencies, keeping logs, noticing an attack and responding to an
incident, preserving evidence, restoring from backup, the cloud, privacy,
ethics and responsible disclosure. This section looks at all of it
together; at the end there are 40 mixed questions and five exercises that
combine several sections.

## Map of the module

| Topic | Main idea |
|---|---|
| **Memory safety** | In languages without bounds checks, overflowing data corrupts neighbouring memory; Python checks bounds itself. |
| **Memory protections** | ASLR, DEP and canaries do not close the hole, they make exploitation harder; layered defence. |
| **Operating system security** | The operating system is the referee: user mode, process isolation, default deny, a standard account for daily work. |
| **File permissions** | Owner, group, others; read, write, execute; a world-writable file is dangerous. |
| **Privilege escalation** | Horizontal and vertical escalation; an ownership check on every request, an allow list for fields from the client. |
| **Secure software development** | Security at every step of the SDLC; fail securely, secure defaults, validate input with an allow list. |
| **Code review and static analysis** | Finding dangerous patterns without running the code; a second pair of eyes in review. |
| **Dependencies and the supply chain** | Pinned versions, comparing with security advisories, look-alike package names, the hash in the lock file. |
| **Secrets management** | A secret is not written in code or the repository; it is read from the environment or a vault, and rotated when it leaks. |
| **Logging and monitoring** | Structured logs, UTC time; personal data and secrets do not go into logs. |
| **Intrusion detection** | Signatures and anomalies; balancing precision and recall; correlating events. |
| **Incident response** | Preparation, detection, containment, eradication, recovery, lessons learned. |
| **Digital forensics** | Evidence hashes, chain of custody, order of volatility, timelines. |
| **Backup and disaster recovery** | 3-2-1, RPO and RTO, restore tests; an untested backup is not a backup. |
| **Cloud security** | Shared responsibility; most incidents are misconfigurations; default deny in IAM. |
| **Privacy and data protection** | Purpose limitation, data minimisation, pseudonyms, k-anonymity, retention periods. |
| **Ethics and law** | Written permission separates a test from an attack; scope, time window, data handling. |
| **Responsible disclosure** | Report privately to the owner first, announce together with the fix. |

## The path of an incident

The module's operations sections come together in a single incident: the
logs are read, a suspicious pattern is noticed, the incident's timeline is
drawn up and personal data is masked in the report.

<figure class="fig">
<div class="flow">
<span class="node">Log lines</span>
<span class="arrow">→</span>
<span class="node acc">Threshold detection</span>
<span class="arrow">→</span>
<span class="node acc">Timeline</span>
<span class="arrow">→</span>
<span class="node ok">Masked report</span>
</div>
<figcaption>The Logging and Monitoring, Intrusion Detection, Digital Forensics and Privacy sections in a single flow.</figcaption>
</figure>

```python
from collections import Counter

LOG = [
    "2026-11-02T09:00:05 FAIL user=ada ip=10.0.0.7",
    "2026-11-02T09:00:09 FAIL user=ada ip=10.0.0.7",
    "2026-11-02T09:00:12 FAIL user=root ip=10.0.0.7",
    "2026-11-02T09:00:15 OK user=ada ip=10.0.0.7",
    "2026-11-02T09:03:40 FAIL user=bob ip=10.0.0.9",
]


def parse(line):
    stamp, status, *pairs = line.split()
    fields = dict(pair.split("=", 1) for pair in pairs)
    return stamp, status, fields["user"], fields["ip"]


events = [parse(line) for line in LOG]
fails = Counter(ip for _, status, _, ip in events if status == "FAIL")
suspects = sorted(ip for ip, count in fails.items() if count >= 3)
print("suspects:", suspects)
for stamp, status, user, ip in events:
    if ip in suspects:
        print(stamp[11:], status, user[0] + "***")
```

```text
suspects: ['10.0.0.7']
09:00:05 FAIL a***
09:00:09 FAIL a***
09:00:12 FAIL r***
09:00:15 OK a***
```

After three failed attempts from the same address, a **successful** login
came: this is no longer just an alert but an incident, and the steps from
the Incident Response section begin (lock the account, close the sessions,
change the password). `10.0.0.9`, with a single failed attempt, did not
reach the threshold. The user names in the report were masked because they
are personal data; the full name is not needed to understand the incident.

## Pairs that get mixed up

| The two | Difference |
|---|---|
| ASLR / DEP | ASLR randomises addresses; DEP stops code running in data areas |
| Horizontal / vertical privilege escalation | Reaching another user's data / a higher role |
| Static analysis / dynamic testing | Reading the code without running it / trying it while it runs |
| Secret / configuration | A value that does harm when leaked / a setting that does not |
| Logging / monitoring | Writing the event / watching what is written and alerting |
| Signature / anomaly-based detection | Looking for a known pattern / looking for deviation from the usual |
| Containment / eradication | Stopping the spread / removing the root cause |
| RPO / RTO | How much data loss / how much downtime is acceptable |
| IDS / IPS | Detects what looks like an attack and alerts / stops it |
| Pseudonym / anonymous | Reversible with the key, data stays personal / identifies no one |
| Coordinated / full disclosure | Together with the fix / without waiting for a fix |

## Summary

- Defence is **layered**: no single protection stops everything, each layer
  makes the attacker's work harder.
- **Least privilege** is the same idea everywhere: file permissions,
  processes, cloud roles, test permission.
- Security belongs to **every stage** of software: design, code,
  dependencies, release.
- The operations cycle: **log, monitor, detect, respond, preserve evidence,
  recover, learn**.
- An **untested backup** and an **untested plan** give no assurance.
- Privacy and ethics decide **how** technical knowledge is used; permission
  is given to what is written.
