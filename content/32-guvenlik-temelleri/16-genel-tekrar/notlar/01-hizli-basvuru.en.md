## Formulas

| What | Calculation |
|---|---|
| Availability | uptime / total time × 100 |
| Qualitative risk | likelihood (1–5) × impact (1–5); 1–4 low, 5–9 medium, 10–16 high, 17–25 critical |
| Single loss expectancy | SLE = asset value (AV) × exposure factor (EF) |
| Annual loss expectancy | ALE = SLE × annual rate of occurrence (ARO) |
| Is the control worth it? | ALE before − ALE after − yearly cost of the control > 0 |
| Password entropy | length × log₂(alphabet size) bits |

## CVSS levels

0.1–3.9 low · 4.0–6.9 medium · 7.0–8.9 high · 9.0–10.0 critical.

## STRIDE

| Letter | Threat | What it breaks |
|---|---|---|
| S | Spoofing | Authenticity |
| T | Tampering | Integrity |
| R | Repudiation | Non-repudiation |
| I | Information disclosure | Confidentiality |
| D | Denial of service | Availability |
| E | Elevation of privilege | Authorization |

## Python tools

| Task | Tool |
|---|---|
| Hash | `hashlib.sha256(data).hexdigest()` |
| Password hash | `hashlib.pbkdf2_hmac("sha256", password, salt, rounds)` |
| Keyed hash | `hmac.new(key, message, hashlib.sha256)` |
| Constant-time comparison | `hmac.compare_digest(a, b)` |
| Secure randomness | `secrets.token_hex(16)`, `secrets.choice(...)` |
| The real owner of an address | `urllib.parse.urlsplit(url).hostname` |

## Access models

DAC the owner decides · MAC the system sets the rule · RBAC role · ABAC
attributes. Bell-LaPadula: no read up, no write down (confidentiality).
Biba: no read down, no write up (integrity).

## Checklists

- **New account:** the role's permissions, multi-factor, owner recorded.
- **Leaver:** every account closed, shared secrets changed, tokens revoked.
- **Token:** format → signature → `iss` → `aud` → `exp` → `nbf`.
- **Suspicious e-mail:** sender domain, the link's real owner, haste, a
  request for a password or payment → report it, verify through another
  channel.
- **Backups:** 3 copies, 2 media, 1 elsewhere, 1 offline; tested.
