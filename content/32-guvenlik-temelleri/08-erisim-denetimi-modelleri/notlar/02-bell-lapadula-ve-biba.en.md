The two models use the same ordered levels but protect different things,
and their rules are the opposite of each other.

| | **Bell-LaPadula** | **Biba** |
|---|---|---|
| What does it protect? | Confidentiality | Integrity |
| Read rule | No read up: level ≥ document | No read down: level ≤ document |
| Write rule | No write down: level ≤ document | No write up: level ≥ document |
| What it fears | Secret information flowing down | Untrusted data flowing up |

## Think of the flow instead of memorising

- **Bell-LaPadula:** information may only flow **up**. Secret information
  must not reach someone below.
- **Biba:** information may only flow **down**. Data from a less trusted
  source must not corrupt a highly trusted system.

## A Bell-LaPadula example

Levels: `public` < `internal` < `secret` < `top-secret`. For someone with
clearance `secret`:

| Document | Can read? | Can write? |
|---|---|---|
| public | Yes | No |
| internal | Yes | No |
| secret | Yes | Yes |
| top-secret | No | Yes |

"Writing up" is in practice like dropping a document into a report box: you
write where someone higher will read it, but you cannot read there.

## A Biba example

Levels: `low` (a file from the internet) < `medium` (an employee's
document) < `high` (the system configuration). For a program at `medium`
level:

| Data | Can read? | Can write? |
|---|---|---|
| low | No | Yes |
| medium | Yes | Yes |
| high | Yes | No |

## Why are both together hard?

If the two models are applied together with the same levels, a person can
only read and write **at their own level**. That is very rigid; so real
systems use separate labels for confidentiality and integrity.
