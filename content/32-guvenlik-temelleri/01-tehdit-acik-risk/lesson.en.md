# Threats, Vulnerabilities and Risk

Four words always come up together in security talk: **asset**,
**threat**, **vulnerability** and **risk**. In everyday language they are
used for one another, but in security each one means something different.
This section separates those four words, and the answer we give them: the
**control**.

Think of a house. The things in the house are **assets**. A burglar walking
around the neighbourhood is a **threat**. A back window that does not lock
is a **vulnerability**. The chance that the burglar finds that window and
gets in, together with what you would lose if he did, is the **risk**. A
lock fitted to the window is a **control**.

## Threat

A **threat** is anything that could harm an asset. It does not have to
cause harm; it is enough that it could. If there is a person or a group
behind a threat, they are called a **threat actor**. Actors differ a lot in
their aims and their capabilities:

- **Curious or inexperienced people:** those who try ready-made tools at
  random. Little capability, but many of them.
- **Criminal groups working for money:** ransomware, stealing card details,
  fraud. Organised and patient.
- **Someone on the inside** (insider): an employee, a former employee or a
  contractor. Already inside, so they stand behind many controls. Not
  always malicious either; an employee who deletes a file by mistake is in
  this group too.
- **People attacking for a cause** (hacktivists): those who want to send a
  political or social message.
- **State-backed groups:** very capable, very patient groups with specific
  targets.

Not every threat has a person behind it. Fire, floods, power cuts and
hardware failures are threats too; they are what breaks availability most
often.

## Vulnerability

A **vulnerability** is a weakness that a threat can use. Vulnerabilities
can be anywhere:

- **In software:** a function that does not check its input, a bug.
- **In configuration:** a share left open to everyone, a default password
  never changed.
- **In a process:** the account of someone who left the company not being
  closed.
- **In people:** believing a fake e-mail and typing a password.

A way of using a vulnerability is called an **exploit**. In this path we
do not write exploits; we only learn why they are possible and how to close
the vulnerability.

A threat and a vulnerability are separate things and **both are needed**.
Without a burglar, an open window costs nothing; if the window is locked,
the burglar cannot get in that way. In security you usually cannot remove
the threat (you cannot stop every attacker in the world), but you can close
the vulnerability.

## Risk

**Risk** combines the **likelihood** that a threat uses a vulnerability to
harm an asset with the **size** of that harm:

<figure class="fig"><div class="flow">
  <span class="node">Threat</span><span class="arrow">→</span>
  <span class="node">Vulnerability</span><span class="arrow">→</span>
  <span class="node">Asset</span><span class="arrow">→</span>
  <span class="node acc">Impact</span>
</div><figcaption>Risk is this whole chain. If one link is missing, there is no risk.</figcaption></figure>

Roughly, think of **risk = likelihood × impact**. An event that is likely
but small (the canteen menu being changed) and an event that is unlikely
but huge (all health records leaking) do not deserve the same attention. We
will turn risk into numbers in the next section, Assessing Risk.

## Control

A **control** is anything done to reduce risk. Controls are split into
three by when they work:

| Type | When it works | Example |
|---|---|---|
| **Preventive** | Before the event, stops it happening | Locks, passwords, firewalls |
| **Detective** | During or after the event, notices it | Cameras, logs, alarms |
| **Corrective** | After the event, undoes the damage | Restoring from backup, patches |

A good system has all three. A system with only preventive controls cannot
notice when a control is one day bypassed; a system with only detective
controls just watches incidents happen.

## Known vulnerabilities: CVE

Vulnerabilities found in software are announced publicly so that the people
using it can protect themselves. Every announced vulnerability gets an
identifier in the shared list called **CVE** (Common Vulnerabilities and
Exposures): `CVE-YEAR-NUMBER`. The year is the year the identifier was
given; the number has at least four digits. Thanks to this identifier,
everyone knows they are talking about the same vulnerability.

The identifiers below are examples; look at their format:

```python
ids = ["CVE-2017-10001", "CVE-2023-20002", "CVE-2025-30003"]
for cve in ids:
    year = int(cve.split("-")[1])
    print(cve, "year:", year, "age:", 2026 - year)
```

```text
CVE-2017-10001 year: 2017 age: 9
CVE-2023-20002 year: 2023 age: 3
CVE-2025-30003 year: 2025 age: 1
```

Even years after their identifier was given, old vulnerabilities keep being
used. The reason is simple: a **patch** (a fixed version) for the
vulnerability has come out, but not everyone has updated their software.
Most attacks do not use new, unknown vulnerabilities but ones whose patch
came out long ago. A newly found vulnerability that has no patch yet is
called a **zero-day**; they are rare but dangerous.

## How heavy is a vulnerability: CVSS

Not every vulnerability is equally dangerous. **CVSS** (Common
Vulnerability Scoring System) gives a vulnerability a score between 0 and
10, by looking at questions such as: can it be reached remotely, is a
password needed, what does it break. The score is also given a
**severity** name:

| Score | Severity |
|---|---|
| 0.0 | None |
| 0.1 – 3.9 | Low |
| 4.0 – 6.9 | Medium |
| 7.0 – 8.9 | High |
| 9.0 – 10.0 | Critical |

A scan or an audit often produces a long list of findings. The first job is
to sort them by score:

```python
findings = [("login page", 7.5), ("old library", 9.8),
            ("verbose errors", 5.3), ("missing header", 3.1)]
for name, score in sorted(findings, key=lambda f: f[1], reverse=True):
    print(f"{score:>4} {name}")
```

```text
 9.8 old library
 7.5 login page
 5.3 verbose errors
 3.1 missing header
```

A CVSS score describes the vulnerability **itself**, not the **risk** in
your system. A vulnerability scored 9.8 on a machine that is never exposed
to the internet and holds unimportant data can be less urgent than one
scored 7.5 on a login page everyone can reach. The score is a starting
point; the decision is made by looking at the asset and the environment.

## Summary

- An **asset** is what is protected, a **threat** is what could harm it, a
  **vulnerability** is the weakness a threat can use, and **risk** is the
  likelihood of the two meeting together with the impact.
- Threat actors range from curious people to state-backed groups; nature
  and failures are threats too.
- Controls are **preventive**, **detective** and **corrective**; a good
  system has all three.
- Known vulnerabilities are named with a **CVE** identifier and scored with
  **CVSS**.
- Most attacks use old vulnerabilities that already have a patch: updating
  is one of the cheapest controls.
