## The 2021 list and the basic defence

| No | Category | Basic defence | Details |
|---|---|---|---|
| A01 | Broken access control | Ownership and permission check on every request; deny by default | Authorization section |
| A02 | Cryptographic failures | TLS, slow salted password hash, `secrets` | Cryptography module |
| A03 | Injection | Parameterised queries, context-aware output encoding | SQL Injection, XSS |
| A04 | Insecure design | Threat modelling, rate limits, abuse scenarios | Threat Modelling |
| A05 | Misconfiguration | Secure defaults, automatic check before going live | This section |
| A06 | Vulnerable and outdated components | Component list, regular updates | Dependencies |
| A07 | Authentication failures | MFA, rate limits, good session management | Authentication Failures |
| A08 | Integrity failures | Hash and signature verification | Digital Signatures |
| A09 | Logging and monitoring failures | Log events, mask secrets, set up alerts | Logging and Monitoring |
| A10 | SSRF | Allow list for targets, checking the address by parsing it | SSRF |

## Patterns from this section

- **Ownership:** `if invoice is None or invoice["owner"] != user: return None`.
- **Parameterised query:** `conn.execute("... WHERE name = ?", (name,))`.
- **Comparing versions:** `tuple(int(p) for p in version.split("."))`; not
  as text.
- **Integrity:** `hashlib.sha256(data).hexdigest() == expected` (the hash
  from a trusted channel).
- **Masking:** `re.sub(r"(password|token)=[^&\s]+", r"\1=***", line)`.

## Sentences to remember

- Authentication asks "who are you?", access control asks "may you do
  this?"; the two are asked separately.
- Data is not interpreted as code.
- The default setting is the secure setting.
- Nothing from outside is used before it is verified.
- A log records the event, not the secret.
