## The 2025 list and the basic defence

| No | Category | Basic defence | Details |
|---|---|---|---|
| A01 | Broken access control (incl. CSRF, SSRF) | Ownership and permission check on every request; deny by default | Authorization, CSRF, SSRF |
| A02 | Misconfiguration | Secure defaults, automatic check before going live | This section |
| A03 | Supply chain failures | Component list, regular updates, pinned versions, trusted sources | Dependencies |
| A04 | Cryptographic failures | TLS, slow salted password hash, `secrets` | Cryptography module |
| A05 | Injection | Parameterised queries, context-aware output encoding | SQL Injection, XSS |
| A06 | Insecure design | Threat modelling, rate limits, abuse scenarios | Threat Modelling |
| A07 | Authentication failures | MFA, rate limits, good session management | Authentication Failures |
| A08 | Integrity failures | Hash and signature verification | Digital Signatures |
| A09 | Logging and alerting failures | Log events, mask secrets, set up alerts | Logging and Monitoring |
| A10 | Exceptional conditions | Fail closed; catch the expected error explicitly | This section |

Differences from the 2021 edition: supply chain (formerly "vulnerable and
outdated components") and exceptional conditions are new; SSRF is no
longer a category of its own and joined A01; injection moved from A03 to
A05 and misconfiguration from A05 to A02.

## Patterns from this section

- **Ownership:** `if invoice is None or invoice["owner"] != user: return None`.
- **Parameterised query:** `conn.execute("... WHERE name = ?", (name,))`.
- **Comparing versions:** `tuple(int(p) for p in version.split("."))`; not
  as text.
- **Integrity:** `hashlib.sha256(data).hexdigest() == expected` (the hash
  from a trusted channel).
- **Masking:** `re.sub(r"(password|token)=[^&\s]+", r"\1=***", line)`.
- **Failing closed:** `except KeyError: return False`; no broad
  `except Exception: return True`.

## Sentences to remember

- Authentication asks "who are you?", access control asks "may you do
  this?"; the two are asked separately.
- Data is not interpreted as code.
- The default setting is the secure setting.
- Nothing from outside is used before it is verified.
- A log records the event, not the secret.
- When an error happens, the answer is "no".
