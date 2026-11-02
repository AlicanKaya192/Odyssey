# Security Policy and Standards

So far we have seen individual measures: password rules, least privilege,
backups, multi-factor authentication. In an organisation these measures
have to be **written down**, **approved** and **the same for everyone**;
otherwise every team does what it thinks best. This section covers the
management side of security: documents, the classification of data,
international standards, and the difference between "we passed the audit"
and "we are secure".

## The layers of documents

Security documents come in four layers from top to bottom; the upper one
says "what and why", the lower one "how".

| Document | What does it say? | Example | Mandatory? |
|---|---|---|---|
| **Policy** | Purpose and principle; approved by top management | "Only authorised people access the organisation's information." | Yes |
| **Standard** | A measurable rule | "Passwords at least 12 characters; multi-factor authentication for remote access." | Yes |
| **Procedure** | Step by step how to do it | "Opening an account for a new employee: 1. ... 2. ... 3. ..." | Yes |
| **Guideline** | Advice, good practice | "Using a password manager is recommended." | No |

A policy is short and lasting; it does not change when technology does.
Standards and procedures are updated more often. A policy carries **top
management's** approval: security is not only the IT team's job but the
organisation's decision. Documents are reviewed at least once a year and
after any major change.

## Classifying data

Protecting all data equally tightly is both expensive and unnecessary.
That is why data is **classified** and, for every class, it is written down
how it is stored and with whom it is shared. Four common levels:

| Level | Example | Rule |
|---|---|---|
| **Public** | An announcement on the website | Anyone may see it |
| **Internal** | Meeting notes | Employees only |
| **Confidential** | Customer list, contracts | Those who need to know; encrypted transfer |
| **Restricted** | Health data, salaries, keys | Named people; encrypted storage, every access logged |

The levels are ordered; a channel can carry data up to a certain level.
Let us write this rule as a small function:

```python
LEVELS = ["public", "internal", "confidential", "restricted"]
channel_max = {
    "website": "public",
    "team-chat": "internal",
    "encrypted-mail": "confidential",
}


def can_share(level, channel):
    if channel not in channel_max:
        return False
    return LEVELS.index(level) <= LEVELS.index(channel_max[channel])


for level in LEVELS:
    chat = can_share(level, "team-chat")
    mail = can_share(level, "encrypted-mail")
    print(f"{level:<13} {chat!s:<5} {mail}")
```

```text
public        True  True
internal      True  True
confidential  False True
restricted    False False
```

There are two details. A channel not on the list (an unknown file-sharing
site) is **refused**: deny by default (Security Principles). Restricted
data is not sent freely over any channel; it has a separate, approved
process. Data has an **owner** (data owner) who decides its class.

## Standards and frameworks

Organisations do not invent security from scratch; they use
**standards** and **frameworks** everyone accepts.

| Name | What? |
|---|---|
| **ISO/IEC 27001** | The requirements of an information security management system (ISMS). An organisation that passes an independent audit gets a **certificate**. It has a list of controls in its annex. |
| **ISO/IEC 27002** | A guide explaining how to apply the controls in 27001. |
| **NIST CSF** | The Cybersecurity Framework; version 2.0 is organised into six functions: **Govern, Identify, Protect, Detect, Respond, Recover**. |
| **CIS Controls** | A practical list of controls in priority order; a good start for small organisations. |
| **PCI DSS** | The industry standard everyone who processes card data must follow. |

Then there are **laws**. For the protection of personal data there is
**KVKK** (Law No. 6698) in Turkey and **GDPR** in the European Union. Both
place duties on organisations that process personal data: stating the
purpose for which data is processed, not collecting more than needed,
keeping it secure, and reporting a data breach to the authority in time. A
standard is optional; a law is not.

## Mapping controls to functions

The six NIST CSF functions make the gaps in a list of controls easy to
see. Let us map every control to a function and count:

```python
FUNCTIONS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]
controls = [
    ("asset inventory", "Identify"),
    ("mfa for staff", "Protect"),
    ("disk encryption", "Protect"),
    ("log monitoring", "Detect"),
    ("backup restore test", "Recover"),
]
counts = {f: 0 for f in FUNCTIONS}
for name, function in controls:
    counts[function] += 1
for f in FUNCTIONS:
    mark = " <- gap" if counts[f] == 0 else ""
    print(f"{f:<9} {counts[f]}{mark}")
```

```text
Govern    0 <- gap
Identify  1
Protect   2
Detect    1
Respond   0 <- gap
Recover   1
```

This organisation has invested in protection but has nothing in two
functions: who governs security (roles, policy, risk decisions) is not
written down, and nobody knows what to do when an incident happens. All the
measures are about "it should not happen"; there is no answer to "what if
it does?".

## Gap analysis

A **gap analysis** compares the controls a standard asks for with the ones
actually in place in the organisation. The result is a list of work to do.

```python
required = ["access-control", "mfa", "backup", "logging", "patching"]
status = {
    "access-control": "yes",
    "mfa": "partial",
    "backup": "yes",
    "logging": "no",
}

done = [c for c in required if status.get(c) == "yes"]
missing = [c for c in required if status.get(c, "no") == "no"]
partial = [c for c in required if status.get(c) == "partial"]
print(f"coverage: {100 * len(done) / len(required):.0f}%")
print("missing:", missing)
print("partial:", partial)
```

```text
coverage: 40%
missing: ['logging', 'patching']
partial: ['mfa']
```

`patching` is not in the status list at all: nobody asked. `status.get(c,
"no")` counts the unknown as "no"; "we don't know" does not mean a control
exists. The half-done `mfa` does not count towards coverage:
multi-factor authentication switched on only for some accounts does
nothing against someone coming in through an account where it is off.

## Compliance is not security

<figure class="fig"><div class="versus">
  <div class="no"><h4>Compliance</h4>The boxes on the auditor's list are ticked. "We have a password policy, we take backups." The audit day is a snapshot.</div>
  <div class="ok"><h4>Security</h4>The controls actually work and are measured all the time. Is the policy applied, are backups restored, does anyone look at the logs?</div>
</div><figcaption>Certified organisations also suffer breaches; a standard is a starting point, not the finish.</figcaption></figure>

Standards are still very valuable: they remind you of forgotten topics,
give a common language and give customers and partners confidence.

## Policy exceptions

Not every rule can be applied in every case: an old machine may not
support multi-factor authentication. Then the rule is not quietly broken; a
written **exception** is opened. A good exception has four things:

- an **owner** (the person who accepts the risk),
- a **reason**,
- an **end date** (an exception without an end is a permanent hole),
- a **compensating control**: that machine is moved to a separate network
  segment and access to it is logged.

An expired exception is either approved again or closed.

## Summary

- Document layers: **policy** (what and why) → **standard** (measurable
  rule) → **procedure** (how) → **guideline** (advice).
- Data is **classified**: public, internal, confidential, restricted; each
  channel carries data up to a certain level, an unknown channel is refused.
- **ISO/IEC 27001** management system and certificate, **NIST CSF** six
  functions, **CIS Controls** priority list, **PCI DSS** card data; the laws
  **KVKK** and **GDPR**.
- A **gap analysis** compares what is required with what is in place; the
  unknown counts as "no".
- **Compliance is not security**; exceptions have an owner, an end date and
  a compensating control.
