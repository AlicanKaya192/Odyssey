## STRIDE

| Letter | Threat | Breaks | Typical control |
|---|---|---|---|
| **S** | Spoofing | Authenticity | Strong authentication, MFA |
| **T** | Tampering | Integrity | Limiting write access, hashes and signatures, TLS |
| **R** | Repudiation | Non-repudiation | Logs that cannot be changed, digital signatures |
| **I** | Information disclosure | Confidentiality | Access control, encryption, error messages that say little |
| **D** | Denial of service | Availability | Rate limits, redundancy, resource quotas |
| **E** | Elevation of privilege | Authorization | Server-side and object-level checks, least privilege |

## STRIDE per element

| Part | Letters to ask |
|---|---|
| External entity | S, R |
| Process | S, T, R, I, D, E |
| Data store | T, R (if it is a log store), I, D |
| Data flow | T, I, D |

## Data flow diagram

- **External entity:** a person or system not under your control.
- **Process:** code that handles data.
- **Data store:** where data sits.
- **Data flow:** data going between parts.
- **Trust boundary:** the line where the level of trust changes; every flow
  that crosses a boundary is examined separately.

## Four questions

1. What are we working on?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good job?
