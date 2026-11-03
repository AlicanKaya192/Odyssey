# Secrets Management

Every program has a few values it must keep hidden: a database password, a
service's API key, the secret key that signs sessions. These are called
**secrets**. In the Code Review and Static Analysis section we saw how to
search source code for secrets with the syntax tree; this section covers
the other side of the coin: **where** secrets are kept, **how** they are
given to the program, how they are kept out of logs, and **when** they are
changed.

The examples are again toys: we do not connect to real environment
variables or a secrets vault; we imitate the environment with a dict.

## A secret does not live in code

A secret written into code goes everywhere the code goes: into the
repository history, backups, developers' computers, maybe a public
repository. Deleting it from the repository is not enough either, because
it stays in the history. Only the secret's **name** lives in the code; its
value comes from outside at run time:

<figure class="fig"><div class="versus">
  <div><h4>Secret in code</h4><code>DB_PASSWORD = "hunter2"</code>. Whoever sees the code sees the secret; changing it means changing the code; it never leaves the history.</div>
  <div><h4>Secret from outside</h4>The code only knows the name <code>DB_PASSWORD</code>. The value comes from an environment variable or a <b>secrets vault</b>; it can differ per environment and is renewed without changing the code.</div>
</div><figcaption>Code should be clean enough to show anyone; secrets live in a separate place with controlled access.</figcaption></figure>

What should a program that reads a secret from the environment do if the
secret is **missing**? The rule from the Secure Software Development
section: **fail closed**. Instead of carrying on with an empty password or
a default value, stop at once:

```python
ENV = {"DB_HOST": "db.internal", "DB_PASSWORD": "s3cr3t-value"}


def get_secret(env, name):
    value = env.get(name, "")
    if not value:
        raise RuntimeError(f"missing secret: {name}")
    return value


print(len(get_secret(ENV, "DB_PASSWORD")))
try:
    get_secret(ENV, "API_TOKEN")
except RuntimeError as error:
    print(error)
```

```text
12
missing secret: API_TOKEN
```

The missing secret was noticed when the program **started**, and the
message contains only the secret's name, not its value. The program wrote
the secret itself nowhere; it printed only its length.

## Keeping secrets out of logs

The place secrets leak most often is log files: a debug line writes the
whole request or the whole configuration and the password goes with it.
Before a log entry is written, fields holding secrets are **redacted**:

```python
import re

PATTERN = re.compile(r"(password|token|secret)=\S+", re.IGNORECASE)


def redact(line):
    return PATTERN.sub(r"\1=***", line)


print(redact("login user=ada password=hunter2 ok"))
print(redact("call api TOKEN=abc123 status=200"))
```

```text
login user=ada password=*** ok
call api TOKEN=*** status=200
```

The key name stayed and its value became `***`; someone reading the log
sees what was hidden but cannot see the secret. When a secret has to be
identified to people (which key is in use?), only its last few characters
are shown instead of the whole: `****1a2b`.

## Finding a secret: entropy

Secret scanners look for leaked secrets in code and history. One way to
find a secret whose name is unknown is to look at **entropy**: a randomly
generated key is much more "scattered" than an ordinary word. Shannon
entropy measures how many bits of information a text carries per
character:

```python
import math
from collections import Counter


def entropy(text):
    counts = Counter(text)
    total = len(text)
    return sum(c / total * math.log2(total / c) for c in counts.values())


for text in ["aaaaaaaa", "password", "q8Zr2LxP0vT7mWk9"]:
    print(f"{text:<18} {entropy(text):.2f}")
```

```text
aaaaaaaa           0.00
password           2.75
q8Zr2LxP0vT7mWk9   4.00
```

The repeated single letter carries 0.00 bits, an ordinary word
2.75 bits, the random-looking key 4.00 bits. Scanners
flag long strings above a certain threshold as "possible secrets". This is
an estimate: not every random-looking string is a secret (a false alarm),
and short secrets or secrets made of words may stay below the threshold.

## Generating a strong secret

When generating a secret, the `secrets` module we saw in the Randomness
section is used, not `random`:

```python
import secrets

token = secrets.token_urlsafe(32)
print(len(token))
print(all(c.isalnum() or c in "-_" for c in token))
```

```text
43
True
```

32 random bytes turned into a 43-character string that can
travel safely in a URL. We did not print the value itself: it differs on
every run, and a secret is not written to the screen either.

## Renewing secrets

The longer a secret lives, the more likely it is to have leaked unnoticed.
That is why secrets are **rotated** regularly: a new value is generated,
systems are moved to it, and the old one is revoked. Finding which secrets
are due for rotation is a date calculation:

```python
from datetime import date

TODAY = date(2026, 11, 1)
SECRETS = [
    ("db-password", date(2026, 9, 20)),
    ("api-token", date(2026, 6, 1)),
    ("signing-key", date(2025, 12, 15)),
]
MAX_DAYS = 90
for name, created in SECRETS:
    age = (TODAY - created).days
    status = "rotate" if age > MAX_DAYS else "ok"
    print(f"{name:<12} {age:>3} days  {status}")
```

```text
db-password   42 days  ok
api-token    153 days  rotate
signing-key  321 days  rotate
```

A secret known or suspected to have leaked is rotated without waiting:
deleting or hiding it is not enough, because the value may already be in
someone else's hands. What makes rotation easy is the secret living in one
place rather than in the code.

## The secrets vault

In organisations, secrets are kept in a **secrets vault** (secrets
manager). The vault stores secrets encrypted, logs who reached which
secret, limits access with least privilege and can rotate on its own. Some
vaults produce **short-lived** secrets: each application gets a password
valid for a few hours, and when the time is up the password becomes
invalid on its own.

## Summary

- A secret **does not live in code**; only its name does, the value comes
  from the environment or a secrets vault.
- If a secret is missing the program **fails closed**: it does not carry
  on with an empty value.
- Secrets are **redacted** before writing logs; only the last characters
  are shown to identify one.
- Secret scanners look at names and **entropy**; this is an estimate.
- Secrets are generated with the `secrets` module and are not written to
  the screen.
- Secrets are **rotated** regularly; a leaked secret is rotated at once.
