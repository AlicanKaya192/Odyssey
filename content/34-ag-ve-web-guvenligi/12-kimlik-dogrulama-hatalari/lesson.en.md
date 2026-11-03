# Authentication Failures

In the Security Fundamentals module we saw the concepts of authentication
(something you know, have, are; MFA) and how passwords are stored. The
Sessions and Cookies section covered what comes **after** login. This
section looks at the mistakes in the login **itself**: messages that give
away user names, unlimited attempts, the password reset flow and weak
password rules. The A07 category of the OWASP Top 10 is the sum of these.
All the examples are small Python functions; no login to a real system is
attempted.

## Giving away the user name

Saying **why** a login failed looks like help for the user, but it helps
the attacker too:

```python
USERS = {"ada", "bob"}


def login_leaky(user, password_ok):
    if user not in USERS:
        return "no such user"
    if not password_ok:
        return "wrong password"
    return "welcome"


def login_safe(user, password_ok):
    if user in USERS and password_ok:
        return "welcome"
    return "invalid user name or password"


for user in ["ada", "zeynep"]:
    print(f"{user:<7} {login_leaky(user, False):<15} {login_safe(user, False)}")
```

```text
ada     wrong password  invalid user name or password
zeynep  no such user    invalid user name or password
```

The first function said that there is no user called `zeynep` and that
`ada` exists. This is called **user enumeration**: the attacker first
learns which accounts exist, then attacks only those. The right way is to
give **the same** message in both cases. The same principle holds on the
sign-up and password reset pages: the message "we sent a link to this
e-mail" is the same whether the address is registered or not.

Time can give things away as much as the message. If no password hash is
computed for an unknown user, the answer comes back faster. That is why the
program in the Overall Review section of Security Fundamentals computed a
hash for an unknown user too.

## Unlimited attempts

If there is no limit, the attacker tries thousands of passwords for one
account (**brute force**), or tries user name–password pairs leaked from
other sites one after another; because people use the same password in
many places, some of these pairs work. This is called **credential
stuffing**.

Locking the account completely after a few failures is the first solution
that comes to mind, but it hands the attacker another weapon: locking
everyone's account on purpose and making them unusable (denial of service
from the Network Attacks section). A more balanced way is an **increasing
delay**: after a few failures, the wait doubles with every new failure, up
to a cap:

```python
def delay_after(failures):
    if failures < 3:
        return 0
    return min(2 ** (failures - 3), 300)


print([delay_after(n) for n in range(1, 12)])
```

```text
[0, 0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
```

Someone who mistypes their password twice does not wait at all; at the
tenth failure the wait is more than two minutes. For an attacker who wants
thousands of attempts a second, this means the attempts practically stop.
The limit is kept **both per account and per source**: in credential
stuffing the attacker tries each account once, but does so for many
accounts from a single source, and that shows in the logs:

```python
from collections import defaultdict

log = [("198.51.100.9", f"user{i}", False) for i in range(25)] + [
    ("192.168.1.10", "ada", False), ("192.168.1.10", "ada", True)]

failed_users = defaultdict(set)
for src, user, ok in log:
    if not ok:
        failed_users[src].add(user)
for src, users in sorted(failed_users.items()):
    print(src, len(users), "SUSPECT" if len(users) >= 10 else "ok")
```

```text
192.168.1.10 1 ok
198.51.100.9 25 SUSPECT
```

Failed logins to 25 different accounts from a single source are the
typical trace of credential stuffing. The strongest defence, though, is
**multi-factor authentication**: a leaked password alone is not enough.

## Password reset

The "I forgot my password" flow is the legitimate way into an account
without knowing the password; so it needs at least as much care as login.
The token in the reset link:

- is made with `secrets` and is unpredictable;
- is **short-lived** (for example 15 minutes);
- is used **once**;
- has its **hash** stored on the server: if the database leaks, the tokens
  cannot be used (like passwords).

```python
import hashlib
import hmac
import secrets

store = {}


def issue(user, now):
    token = secrets.token_urlsafe(32)
    digest = hashlib.sha256(token.encode()).hexdigest()
    store[user] = {"hash": digest, "expires": now + 900, "used": False}
    return token


def redeem(user, token, now):
    record = store.get(user)
    if record is None or record["used"] or now >= record["expires"]:
        return False
    digest = hashlib.sha256(token.encode()).hexdigest()
    if not hmac.compare_digest(record["hash"], digest):
        return False
    record["used"] = True
    return True


token = issue("ada", 0)
print(redeem("ada", "guess", 10))
print(redeem("ada", token, 20))
print(redeem("ada", token, 30))
late = issue("ada", 0)
print(redeem("ada", late, 1000))
```

```text
False
True
False
False
```

The wrong token was refused; the right token worked once and was refused
on its second use; the token past 900 seconds was refused too. After the
password changes, **all the person's other sessions** are closed (the
Sessions and Cookies section): the reason for changing it may be that
someone is already inside.

A fast hash (SHA-256) is enough for the token's hash here: unlike a
password, the token is a 256-bit random value and cannot be found by
guessing. Passwords need a slow hash because people choose guessable
passwords.

## Password rules

Old rules said "one capital, one digit, one symbol, change every 90 days";
the result was guessable passwords such as `Password1!` and notes written
on paper. Today's approach (the Passwords section) rests on **length** and
on **rejecting known bad passwords**:

```python
COMMON = {"123456", "password", "qwerty", "iloveyou", "admin123"}


def password_problems(password, user):
    problems = []
    if len(password) < 8:
        problems.append("too short")
    if password.lower() in COMMON:
        problems.append("common")
    if user.lower() in password.lower():
        problems.append("contains user name")
    return problems


for pw in ["qwerty", "Ada2026!", "blue-river-under-stone"]:
    print(f"{pw:<24} {password_problems(pw, 'ada')}")
```

```text
qwerty                   ['too short', 'common']
Ada2026!                 ['contains user name']
blue-river-under-stone   []
```

Real systems use, instead of `COMMON`, a list of millions of passwords seen
in leaks. The long password that does not contain the user name passed. A
password is changed only when there is a sign of a leak, not by the
calendar; using a password manager is encouraged.

## Other common mistakes

- **Default passwords:** the `admin/admin` account that came with the
  installation stays live (overlaps with A02 in the OWASP Top 10).
- **Carrying credentials in the URL:** a password or token in the address
  goes into logs and the `Referer` (the HTTP and HTTPS section).
- **Leaving MFA skippable:** if the MFA step is a separate page and the
  server treats the session as fully authorised without checking that the
  second step was completed, MFA stays on paper.
- **Not logging login attempts:** failed and successful logins are logged
  with source and time (not the password).

## Summary

- On a failed login, **a single message**: "invalid user name or
  password"; the timing does not give it away either.
- Against **brute force** and **credential stuffing**: limits per account
  and per source, an **increasing delay**, and above all **MFA**. Locking
  completely opens the door to denial of service.
- The **reset token** is random, short-lived, single-use and hashed on the
  server; when the password changes, the other sessions are closed.
- The **password rule** is length and rejecting known bad passwords; not
  forced periodic changes or complexity rules.
- Default passwords are removed, credentials are not put in URLs, MFA is
  checked on the server, logins are logged.
