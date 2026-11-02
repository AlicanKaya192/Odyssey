# Identity Management and Single Sign-On

The Authentication section described a single login: "is this person
really Ada?". An organisation, however, has hundreds of people, dozens of
systems and roles that change every day. **Identity and access management**
(IAM) brings order to this crowd: who gets an account, which permissions
are given, what happens when a role changes, which doors close when someone
leaves. The second half of this section is about logging in once in one
place instead of separately to every system: **single sign-on** (SSO).

## The life cycle of an account

An account's life is described by three events, **JML** after their
initials:

| Event | What happens? | Common mistake |
|---|---|---|
| **Joiner** | A new employee gets accounts according to their role. | Giving extra permissions "because we don't know what they'll need". |
| **Mover** | The role changes; the new role's permissions are added and **the old ones removed**. | Only adding: over the years the person collects the permissions of every role (privilege creep from the Least Privilege section). |
| **Leaver** | Every account is closed, shared secrets they knew are changed, devices are returned. | Forgetting one system. |

A forgotten account of an employee who has left is called an **orphaned
account**. Nobody uses it, so its password never changes, nobody looks at
it, and it is a quiet door for an attacker. Finding orphaned accounts is
simple: compare the **list of active employees** from human resources with
the list of accounts in every system.

```python
active = {"ada", "bora", "ceren"}
accounts = {
    "mail": ["ada", "bora", "ceren", "deniz"],
    "wiki": ["ada", "deniz"],
    "payroll": ["ceren", "emre"],
}
for system, users in accounts.items():
    for user in users:
        if user not in active:
            print(f"{system:<8} {user:<6} orphaned")
```

```text
mail     deniz  orphaned
wiki     deniz  orphaned
payroll  emre   orphaned
```

`deniz` was forgotten in two systems, `emre` in the payroll system. This
comparison is made regularly (once a month, for example); it is called an
**access review**. Every manager is shown their team's permissions and
asked "is this still needed?".

There are accounts that do not belong to a person too: the **service
account** a program uses to connect to a database. These also need an
owner; a service account whose owner has left is the most dangerous kind
of orphaned account, because it usually has wide permissions and its
password does not change for years.

## Central identity

If every system keeps its own user list, JML is done separately in each
system and one of them is always forgotten. The solution is to keep
identities in **one place**: a **directory**. People, groups and roles live
there; systems ask the directory about a person. When a leaver's record is
closed in the directory, the door of every system that depends on it closes
at once. The common standard for reaching directories is **LDAP**.

## Single sign-on (SSO)

**Single sign-on** (SSO) lets a person log in once and use many
applications without entering a password again. There are two sides:

- **Identity provider** (IdP): where the person actually logs in. Only it
  sees the password and the multi-factor authentication.
- **Service provider** (SP): the application the person wants to use. It
  never sees the password; it trusts the IdP's **signed** statement saying
  "this is Ada".

<figure class="fig"><div class="flow">
  <span class="node">Application (SP)</span><span class="arrow">→</span>
  <span class="node acc">IdP: password + second factor</span><span class="arrow">→</span>
  <span class="node">Signed token</span><span class="arrow">→</span>
  <span class="node">SP checks the signature</span><span class="arrow">→</span>
  <span class="node ok">Inside</span>
</div><figcaption>With single sign-on the password only goes to the identity provider; the application trusts the signed token.</figcaption>
</figure>

Different organisations trusting each other's identities is called
**federation**: like a university student logging in to another
institution's library system with their own school account.

**Benefits:** the person remembers one strong password (less password
reuse); multi-factor authentication is enforced in one place; a leaver's
access is closed in one place; every login is logged in one place.

**Risk:** all the eggs are in one basket. Whoever takes over the IdP gets
into every application, and if the IdP goes down nobody can log in
anywhere. That is why IdP accounts are protected with strong multi-factor
authentication and the IdP itself is among the most closely watched
systems.

## Standards

| Standard | What for? | Document |
|---|---|---|
| **SAML 2.0** | Enterprise single sign-on (mostly web) | A signed **assertion** in XML |
| **OAuth 2.0** | **Delegation**: giving an application limited permission to act on your behalf without giving it your password | **Access token** |
| **OpenID Connect** (OIDC) | An **identity** layer on top of OAuth 2.0: "who logged in?" | **ID token**, in JWT format |

<figure class="fig"><div class="versus">
  <div><h4>OAuth 2.0</h4>"This application may <b>read</b> my calendar." It grants a <b>permission</b>. An access token is not designed to say who logged in; using it alone for login is a common mistake.</div>
  <div><h4>OpenID Connect</h4>"The person who logged in is <b>Ada</b>, verified by this identity provider." It states an <b>identity</b>. The ID token answers whose, for whom and until when.</div>
</div><figcaption>OAuth is delegation, OpenID Connect is authentication; "log in with OAuth" usually means OIDC.</figcaption></figure>

## A signed token

The token the IdP gives is a piece of text that carries information and is
**signed**. The common format is **JWT** (JSON Web Token): three parts
separated by dots: `header.body.signature`. The body is JSON encoded with
base64. Here we see the same idea with a small two-part **toy** token: a
body and an HMAC signature (the keyed hash from the Password Storage
section). In a real application tokens are made and checked with a
library; they are not written by hand.

```python
import base64
import hashlib
import hmac
import json

KEY = b"toy-shared-key-for-the-lesson"


def sign(text):
    return hmac.new(KEY, text.encode(), hashlib.sha256).hexdigest()


def make_token(claims):
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode()
    return body + "." + sign(body)


def read_token(token):
    body, signature = token.split(".")
    if not hmac.compare_digest(signature, sign(body)):
        return "bad signature"
    return json.loads(base64.urlsafe_b64decode(body))


token = make_token({"sub": "ada", "role": "user"})
print(read_token(token))
body, signature = token.split(".")
print(base64.urlsafe_b64decode(body))

fake = json.dumps({"sub": "ada", "role": "admin"}).encode()
forged = base64.urlsafe_b64encode(fake).decode() + "." + signature
print(read_token(forged))
```

```text
{'sub': 'ada', 'role': 'user'}
b'{"sub": "ada", "role": "user"}'
bad signature
```

Two things show up:

1. **A signature does not hide.** On the second line we decoded the body
   without the key; anyone who sees the token can read it. No password or
   secret goes into a token.
2. **A signature catches changes.** The token whose body was changed from
   `user` to `admin`, with the old signature attached, was rejected:
   without the key nobody can produce a new signature.

That is why the order matters: **signature first, content second.**
Trusting the `role` field of a token whose signature was not checked means
trusting a permission the person wrote themselves. Real JWT has one more
trap: the header names the algorithm, and some old libraries accepted an
unsigned token saying "no algorithm" (`none`). The server **decides itself
which algorithm it expects**; it does not go by what the token says.

## The signature is right, but is the token valid?

A correct signature is not enough. The **claims** in the token's body are
checked too:

| Claim | Meaning | Check |
|---|---|---|
| `iss` (issuer) | Who issued the token? | Is it an IdP we trust? |
| `aud` (audience) | Who is the token for? | Is it for our application? |
| `sub` (subject) | Who does the token describe? | The person's identity |
| `exp` (expiration) | Valid until when? | Has it expired? |
| `nbf` (not before) | Valid since when? | Is it too early? |

The `aud` check is often forgotten: if a token the same IdP issued for the
**library application** is accepted by the **grades system**, someone who
sees the token in the library gets into the grades system too.

```python
def check(claims, now):
    if claims.get("iss") != "https://id.school.example":
        return "wrong issuer"
    if claims.get("aud") != "grades-app":
        return "wrong audience"
    if now >= claims.get("exp", 0):
        return "expired"
    return "ok"


claims = {
    "iss": "https://id.school.example",
    "aud": "grades-app",
    "sub": "ada",
    "exp": 1000,
}
print(check(claims, 900))
print(check(claims, 1000))
print(check({**claims, "aud": "library-app"}, 900))
```

```text
ok
expired
wrong audience
```

Time is a small number here; in reality `exp` is the number of seconds
since 1970. Tokens are kept short-lived (minutes) so that a stolen token is
useful only briefly. For a long session a separate **refresh token** is
used, and it can be revoked.

## Logging out

Single sign-on has a partner, **single logout**: logging out of the IdP
should also end the sessions in the connected applications. If a leaver's
IdP account is closed while they still hold a valid token, they can stay
inside until the token expires; that is another reason for short token
lifetimes.

## Summary

- The account life cycle is **JML**: joiner, mover, leaver. For a mover the
  old permissions are removed; for a leaver no system is forgotten.
- **Orphaned accounts** are found by comparing against the list of active
  employees; access is reviewed regularly.
- In **SSO** the password only goes to the **IdP**; the **SP** trusts the
  signed token. Benefit: one strong login, closing in one place; risk: the
  IdP is a single target.
- **SAML** is enterprise SSO, **OAuth 2.0** is delegation, **OpenID
  Connect** is identity.
- In a token, **signature** first, then the **claims**: `iss`, `aud`,
  `exp`, `nbf`. A signature does not hide the content.
