# The OWASP Top 10

So far the module has explained the road: the network, DNS, HTTP,
sessions. From here on it looks at the application itself, that is, at
the holes in a website's code. The most widely used reference in this area
is the **OWASP Top 10**. This section introduces the list as a map; it
shows each heading with a small, self-contained example followed straight
away by its defence. The later sections (SQL Injection, XSS, CSRF, SSRF,
Authentication Failures) will go into the details.

## What are OWASP and the Top 10?

**OWASP** (the Open Worldwide Application Security Project) is a
non-profit community that produces open, free resources on application
security. The **Top 10** is its best-known document: based on data
collected from many organisations and on expert opinion, it ranks the ten
**risk categories** seen as most important in web applications. It is not a
checklist or a standard but an **awareness** document: the answer to
"where are mistakes made most often?".

The list is updated every few years; the order and names of the categories
can change from edition to edition, and the current edition is checked in
OWASP's own publication. Below we use the **2025 edition**.

<figure class="fig anat">
  <div class="anat-row"><span><b>A01</b> Broken access control</span><span>A person can reach data or actions they have no permission for (CSRF and SSRF are here too).</span></div>
  <div class="anat-row"><span><b>A02</b> Security misconfiguration</span><span>Debugging left on, default passwords, unnecessary features.</span></div>
  <div class="anat-row"><span><b>A03</b> Software supply chain failures</span><span>A vulnerable or malicious library, or a broken build and distribution pipeline.</span></div>
  <div class="anat-row"><span><b>A04</b> Cryptographic failures</span><span>Sensitive data is unencrypted, protected with a weak algorithm or with misused crypto.</span></div>
  <div class="anat-row"><span><b>A05</b> Injection</span><span>User data is interpreted as code (SQL, commands, scripts; XSS is here too).</span></div>
  <div class="anat-row"><span><b>A06</b> Insecure design</span><span>The hole is not in the code but in the design: a needed check was never thought of.</span></div>
  <div class="anat-row"><span><b>A07</b> Authentication failures</span><span>Weak password rules, a login open to brute force, poor session management.</span></div>
  <div class="anat-row"><span><b>A08</b> Software or data integrity failures</span><span>An update, plugin or data used without verification.</span></div>
  <div class="anat-row"><span><b>A09</b> Security logging and alerting failures</span><span>Attacks are not logged, nobody is told, or the logs leak secrets.</span></div>
  <div class="anat-row"><span><b>A10</b> Mishandling of exceptional conditions</span><span>When an error happens, the program leaves the door open or ends up in an inconsistent state.</span></div>
  <figcaption>The OWASP Top 10, 2025 edition. The order follows the risk assessment.</figcaption>
</figure>

In older sources you will meet the 2021 edition; its numbers differ (there
injection is A03 and misconfiguration A05). Two categories are new in 2025:
**supply chain** (a wider form of the 2021 category "vulnerable and
outdated components") and **exceptional conditions**. **SSRF**, a category
of its own in 2021, was folded into broken access control. The ideas the
categories describe stayed largely the same.

## A01 Broken access control

The category at the top of the list describes the most common mistake: the
application checks **who** is asking but not whether they are allowed
**what** they are asking for. Its most typical form is reaching someone
else's record by changing the number in the address (`/invoices/102`). This
is called an **insecure direct object reference** (IDOR).

```python
INVOICES = {101: {"owner": "ada", "amount": 250},
            102: {"owner": "bob", "amount": 990}}


def get_invoice_bad(user, invoice_id):
    return INVOICES.get(invoice_id)


def get_invoice(user, invoice_id):
    invoice = INVOICES.get(invoice_id)
    if invoice is None or invoice["owner"] != user:
        return None
    return invoice


print(get_invoice_bad("ada", 102))
print(get_invoice("ada", 102))
print(get_invoice("ada", 101))
```

```text
{'owner': 'bob', 'amount': 990}
None
{'owner': 'ada', 'amount': 250}
```

The first function gave Ada Bob's invoice. The right way is to check the
record's owner **on every request** (complete mediation from the Security
Principles section). Missing and forbidden give the same answer (`None`,
404 in HTTP); as we saw in the HTTP and HTTPS section, this way not even
the existence of someone else's invoice is revealed.

This category also covers two familiar holes. In **CSRF** the person's
browser, and in **SSRF** the server, uses its own permission to do a job
someone else asked for. The problem is the same in both: the request is
handled without its permission being checked. The CSRF and SSRF sections
will cover them separately.

## A02 Security misconfiguration

Even when the code is right, the settings can leave things open: debug mode
left on (the error page shows code and settings), the default admin
password, directory listing, allowing plain HTTP. These can be checked
automatically:

```python
config = {"debug": True, "admin_password": "admin",
          "dir_listing": False, "https_only": False}

problems = []
if config["debug"]:
    problems.append("debug mode is on")
if config["admin_password"] in {"admin", "password", "1234"}:
    problems.append("default admin password")
if config["dir_listing"]:
    problems.append("directory listing is on")
if not config["https_only"]:
    problems.append("plain HTTP allowed")
for problem in problems:
    print("-", problem)
```

```text
- debug mode is on
- default admin password
- plain HTTP allowed
```

Running such a check before going live catches most configuration
mistakes. Defaults are chosen to be safe: the "secure defaults" from the
Security Principles section.

## A03 Software supply chain failures

Applications rest on hundreds of libraries, and on the tools that build and
distribute them. If any link in this chain breaks, the application breaks
too: a library with a known hole, a hijacked package, a tampered build tool.
The most common case is the simplest: when a hole is published in a
library, everyone who does not update is exposed. Even checking which
version is current has a trap, because version numbers cannot be compared
as text:

```python
def parse(version):
    return tuple(int(p) for p in version.split("."))


print("1.10.0" < "1.9.0")
print(parse("1.10.0") < parse("1.9.0"))

installed = {"pagekit": "2.4.1", "imagelib": "1.10.0", "parser": "0.9.3"}
minimum = {"pagekit": "2.4.1", "imagelib": "1.9.2", "parser": "1.0.0"}
for name, version in installed.items():
    ok = parse(version) >= parse(minimum[name])
    print(f"{name:<9} {version:<7} {'ok' if ok else 'UPDATE'}")
```

```text
True
False
pagekit   2.4.1   ok
imagelib  1.10.0  ok
parser    0.9.3   UPDATE
```

As text `"1.10.0"` looks smaller (`1` < `9`); as numbers it is bigger.
Defence: keeping a list of components, watching vulnerability notices,
updating regularly, removing components that are not used, pinning
versions and taking packages only from trusted sources (the Dependencies
and the Supply Chain section of the System Security module).

## A04 Cryptographic failures

The subject of the Cryptography module: a password stored as plain text or
with a fast hash, data carried without HTTPS, a key written into the code,
predictable randomness. The defence is that module's rules: a slow, salted
hash for passwords (the Storing Passwords section), TLS in transit,
`secrets` for randomness, not writing your own crypto.

## A05 Injection

The heart of injection is one sentence: **the user's data is interpreted as
part of the code.** Its best-known example is SQL. Building a query by
joining text pastes the data into the query. No malice is even needed;
someone with an apostrophe in their name is enough:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, city TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)",
                 [("Ada", "Istanbul"), ("O'Brien", "Izmir")])

name = "O'Brien"
try:
    query = "SELECT city FROM users WHERE name = '" + name + "'"
    print(conn.execute(query).fetchall())
except sqlite3.OperationalError as error:
    print("error:", error)

print(conn.execute("SELECT city FROM users WHERE name = ?", (name,)).fetchall())
```

```text
error: near "Brien": syntax error
[('Izmir',)]
```

In the joined query, the `'` in the name closed the text early and the rest
was read as SQL syntax: the query broke. Someone who causes this accidental
breakage on purpose can change the query's meaning. The right way is a
**parameterised query** (the second line): the query and the data are sent
separately, and the database always treats what comes in place of `?` as
**data**. The SQL Injection section will go into this in detail; the same
idea holds for the command line (not building a command from text) and for
HTML (encoding output in the XSS section).

## A06 Insecure design

Some holes are not in a line of code but in the **design**. If there is no
limit on requesting a password-reset code, a four-digit reset code is found
in 10000 attempts, however cleanly the code is written. The defence is at
the design stage: threat modelling (the Threat Modelling and STRIDE
section), rate limits, thinking through abuse scenarios from the start.

## A07 Authentication failures

A login form open to brute force, weak or default passwords, no
multi-factor authentication (MFA), a session ID that is predictable or not
renewed at login. The Sessions and Cookies section covered the session side
of this; the Authentication Failures section will cover the login side.

## A08 Software or data integrity failures

If the application uses an update, a plugin or data from outside **without
verifying it**, whoever changes it on the way or at its source gets inside
the application. The difference from the supply chain category is scale:
there the whole chain, here a single package or piece of data. The simplest
check is comparing with a hash obtained over a trusted channel (the Hash
Functions section):

```python
import hashlib

update = b"toy update package v2"
published = hashlib.sha256(update).hexdigest()


def safe_to_install(data, expected):
    return hashlib.sha256(data).hexdigest() == expected


print(safe_to_install(update, published))
print(safe_to_install(update + b" + extra", published))
```

```text
True
False
```

The package with extra bytes added was refused. A hash only helps if it came
**over a trusted channel**; someone who changes a hash that comes from the
same place as the package changes both together. That is why updates are
signed with digital signatures (the Digital Signatures section).

## A09 Security logging and alerting failures

If an attack is not logged, it is not noticed; if it is logged but nobody
is told, it is still not stopped. That is why the 2025 edition puts
**alerting** in the category's name: a log alone is not enough, an
important event has to reach someone. Logs need care too: **passwords,
tokens and session IDs are not written into logs**, otherwise anyone who
can read the logs takes over the accounts. These values are masked before
logging:

```python
import re


def mask(line):
    return re.sub(r"(password|token)=[^&\s]+", r"\1=***", line)


print(mask("login user=ada&password=s3cret&next=/home"))
print(mask("api call token=abc123 status=200"))
```

```text
login user=ada&password=***&next=/home
api call token=*** status=200
```

The regular expression replaced the value that starts with `password=` or
`token=` and runs up to `&` or a space with `***`; it kept the name, so the
log stayed readable. A good log records what happened (who, when, what,
the result), not the secret (the Logging and Monitoring section of the
System Security module).

## A10 Mishandling of exceptional conditions

Programs must stay safe not only when everything is fine but also when
something goes wrong: a missing file, broken data, an unexpected user. The
most dangerous mistake is **failing open**: the program saying "allow" when
an exception happens during a check.

```python
PERMISSIONS = {"ada": {"read", "delete"}}


def can_delete_bad(user):
    try:
        return "delete" in PERMISSIONS[user]
    except Exception:
        return True


def can_delete(user):
    try:
        return "delete" in PERMISSIONS[user]
    except KeyError:
        return False


print(can_delete_bad("bob"))
print(can_delete("bob"))
print(can_delete("ada"))
```

```text
True
False
True
```

For Bob, who is not in the list, `PERMISSIONS["bob"]` raised a `KeyError`;
the first function caught every error and **allowed** the action. The right
way is **failing closed**: the expected error is caught explicitly and the
answer is "no". A broad `except Exception` that silences every error both
opens this hole and hides the real error (the "secure defaults" from the
Security Principles section).

## How to use the list

<figure class="fig"><div class="versus">
  <div class="ok"><h4>Good use</h4>As the team's shared language, in training, and in code review to ask "which category does this change touch?".</div>
  <div class="no"><h4>Bad use</h4>Saying "we closed the ten items, the application is secure". The list describes the most common, not everything; the application's own risks are found with threat modelling.</div>
</div><figcaption>The Top 10 is a starting point, not a finish line.</figcaption></figure>

## Summary

- The **OWASP Top 10** is an awareness document ranking the ten most
  important risk categories in web applications; it is updated every few
  years. The 2025 edition was used here.
- **A01 Broken access control:** the record's owner is checked on every
  request; missing and forbidden give the same answer. CSRF and SSRF are in
  this category too.
- **A02 Configuration:** debugging off, no default passwords; an automatic
  check before going live.
- **A03 Supply chain:** versions are compared as numbers; regular updates,
  trusted sources.
- **A05 Injection:** data must not be interpreted as code;
  **parameterised queries**.
- **A08 Integrity:** a package from outside is not used before it is
  verified with a hash or a signature.
- **A09 Logging and alerting:** attacks are logged and someone is told,
  secrets are not logged (masking).
- **A10 Exceptional conditions:** fail closed when an error happens; do not
  silence errors with a broad `except`.
- The list is a start; risks specific to the application are found with
  threat modelling.
