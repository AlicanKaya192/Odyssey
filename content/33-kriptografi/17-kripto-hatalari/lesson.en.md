# Common Cryptography Mistakes

Cryptography flaws usually come not from an algorithm being broken but
from the right algorithm being **used the wrong way**. This section
gathers the mistakes we met one by one across the module, and shows ways to
**find** them in code or in settings. They all share the same lesson:
cryptography is not written by yourself; it is used through a well-tested
library with the right settings.

## Encoding is not encryption

Base64, hex or URL encoding turns data into **another notation**; there is
no key, and anyone can turn it back.

```python
import base64

token = base64.b64encode(b"user=ada;role=admin")
print(token)
print(base64.b64decode(token))
```

```text
b'dXNlcj1hZGE7cm9sZT1hZG1pbg=='
b'user=ada;role=admin'
```

"It looks unreadable" does not mean it is secret. If confidentiality is
needed, use authenticated encryption; if it must not be changed, HMAC or a
signature.

## The right randomness for a secret value

Every value that **must not be guessed**, such as a key, nonce, salt,
session token or password reset code, is made with the `secrets` module.
The `random` module is made for jobs such as simulations and games; it is
not used for secret values.

```python
import secrets

print(len(secrets.token_bytes(32)))
print(len(secrets.token_hex(16)))
print(len(secrets.token_urlsafe(16)) >= 16)
```

```text
32
32
True
```

## Secrets built into code

A key in the source code is the key of everyone with access to the
repository, and it is not easily removed from git history. The **name** of
a secret may appear in code, but its value must come from an environment
variable or a secret vault. Let us write a simple scanner and search a
sample file:

```python
import re

source = """API_URL = "https://api.example.test"
SECRET_KEY = "s3cr3t-value"
password = os.environ["DB_PASSWORD"]
timeout = 30"""
pattern = re.compile(r'(key|secret|password|token)\w*\s*=\s*["\']', re.IGNORECASE)
for number, line in enumerate(source.splitlines(), 1):
    if pattern.search(line):
        print(number, line.split("=")[0].strip())
```

```text
2 SECRET_KEY
```

The scanner caught only the secret whose **value is written in quotes**;
the password read from an environment variable is fine. In real projects
ready-made secret scanners do this job, run as pre-commit checks. If a
leaked secret is found, deleting it is not enough: it is **changed**
(rotated), because it may remain in the history.

## A catalog of mistakes

| Mistake | Why it is wrong | The right way | Section |
|---|---|---|---|
| Taking encoding for encryption | It has no key | AEAD | This section |
| `random` for a secret value | Predictable | `secrets` | This section |
| A key built into code | Everyone who sees the repo knows it | Environment variable, secret vault | This section |
| Storing a password with a fast hash | Guessing is very fast | A salted, slow KDF | Key Derivation |
| MD5 / SHA-1 for integrity | Collisions can be made | SHA-256 and above | Hash Functions |
| Comparing a tag with `==` | Timing can leak information | `hmac.compare_digest` | Message Authentication: HMAC |
| ECB mode | The pattern leaks | GCM | Block Cipher Modes and IVs |
| Reusing a nonce / IV | The keystream repeats | Unique for every message | Symmetric Encryption |
| Encryption without authentication | Changes go unnoticed | AEAD, verify first | Authenticated Encryption |
| One key for everything | The operations weaken each other | Separate keys with HKDF | Key Derivation |
| RSA without padding | Deterministic | OAEP, PSS | RSA |
| A short key | Open to brute force | AES-128+, RSA-2048+, 256-bit curve | What Is Cryptography? |
| Turning certificate verification off | You do not know whom you talk to | Always on | Certificates and PKI |
| An old TLS version | Known weaknesses | TLS 1.3 / strong TLS 1.2 | The TLS Handshake |
| Writing your own algorithm | Weaknesses that go unnoticed | A well-tested library | What Is Cryptography? |

## Auditing the settings

Most mistakes show up in a configuration file. Writing a small **auditor**
that checks a configuration line by line stops a wrong setting from
reaching production. In the exercises you will build one step by step: a
weak hash name, a short key, a secret built into code, ECB, a fixed nonce,
TLS verification turned off.

## Summary

- Encoding (Base64) is not encryption.
- Secret values are made with `secrets`, not with `random`.
- Secrets are not written into code; a leaked secret is changed.
- Every rule of correct use from the module is in one catalog: mode, nonce,
  authentication, KDF, key size, padding, certificate, TLS version.
- Cryptography is not written by yourself; a well-tested library with the
  right settings.
