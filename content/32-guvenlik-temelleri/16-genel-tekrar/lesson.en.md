# Overall Review

This module built the basic language of security: what we protect, what we
protect it against, how it is decided who may access what, and how all this
is managed in an organisation. This section looks at everything together;
at the end there are 40 mixed questions and five exercises that combine
several sections.

## A map of the module

| Topic | Main idea |
|---|---|
| **The CIA triad** | Confidentiality, integrity, availability; every incident breaks at least one. |
| **Threat, vulnerability, risk** | When a threat uses a vulnerability the asset is harmed; risk = likelihood × impact. CVE is a vulnerability's name, CVSS its weight. |
| **Risk assessment** | A qualitative 1–5 scale or in money (SLE = AV × EF, ALE = SLE × ARO). Four answers: reduce, transfer, accept, avoid. |
| **Security principles** | Least privilege, deny by default, fail securely, defence in depth, complete mediation, open design, simplicity, separation of duties. |
| **Authentication** | Something you know, have, are; multi-factor means different kinds. TOTP makes a code from the time. |
| **Passwords** | Strength = entropy (length × log₂ alphabet); length gains more than complexity. |
| **Password storage** | Neither plain text nor encryption: a salted, slow hash (such as PBKDF2), constant-time comparison. |
| **Authorization** | Subject, action, object; the decision on the server; horizontal and vertical privilege escalation. |
| **Access models** | DAC decides by owner, MAC by rule, RBAC by role, ABAC by attributes. |
| **Least privilege** | Privilege creep, unused permissions, time-limited permissions, separation of duties. |
| **Threat modelling** | Data flow diagram, trust boundaries, STRIDE. |
| **Attack surface** | Inventory, weighing entry points, closing what is unused. |
| **Social engineering** | Uses trust, haste and authority; look at the real owner of a domain; the defence is process. |
| **Malware** | Kinds by spread and behaviour; signature- and behaviour-based detection; 3-2-1 backups. |
| **Identity management** | JML, orphaned accounts, SSO, IdP and SP; in a token the signature first, then the claims. |
| **Policy and standards** | Policy → standard → procedure → guideline; data classes; ISO/IEC 27001, NIST CSF; compliance is not security. |

## The path of a request

Most parts of the module meet on the path of a single request:

<figure class="fig"><div class="flow">
  <span class="node">Request</span><span class="arrow">→</span>
  <span class="node acc">Authentication</span><span class="arrow">→</span>
  <span class="node acc">Authorization</span><span class="arrow">→</span>
  <span class="node">Log</span><span class="arrow">→</span>
  <span class="node ok">Response</span>
</div><figcaption>First "who are you?", then "are you allowed to do this?", and log it in every case.</figcaption></figure>

The small program below does this from start to finish: it checks the
password with a salted, slow hash (Password Storage), allows by role
(Access Control Models), refuses everything it does not know (Security
Principles) and writes every attempt to the log.

```python
import hashlib
import hmac

SALT = b"fixed-salt-for-the-lesson"


def hash_password(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, 100_000).hex()


users = {"ada": {"hash": hash_password("blue-river-42"), "role": "editor"}}
roles = {"viewer": {"read"}, "editor": {"read", "write"}}
log = []


def request(user, password, action):
    record = users.get(user)
    known = record["hash"] if record else ""
    if not hmac.compare_digest(known, hash_password(password)):
        result = "denied: authentication"
    elif action not in roles[record["role"]]:
        result = "denied: authorization"
    else:
        result = "allowed"
    log.append(f"{user} {action} {result}")
    return result


print(request("ada", "blue-river-42", "write"))
print(request("ada", "wrong", "write"))
print(request("ada", "blue-river-42", "delete"))
print(request("zeynep", "x", "read"))
print(len(log), "log lines")
```

```text
allowed
denied: authentication
denied: authorization
denied: authentication
4 log lines
```

Watch the small details: the password hash is computed for an unknown user
too, so the response time does not give away "does such a user exist?". On
an authentication failure it does not say which part (name or password) was
wrong. `delete` is in no role, so it is refused on its own: if a permission
was not written, it does not exist. In a real system the salt is separate
and random for every user; here it is fixed so the result is the same on
every run.

## Pairs that get mixed up

| Pair | Difference |
|---|---|
| Authentication / authorization | "Who are you?" / "Are you allowed to do this?" |
| Threat / vulnerability | The thing that can do harm / the weakness it uses |
| Hash / encryption | Cannot be reversed / opened again with a key |
| Confidentiality / integrity | No unauthorised person reads it / no unauthorised person changes it |
| ACL / capability list | The object's list / the subject's list |
| Bell-LaPadula / Biba | Protects confidentiality / protects integrity |
| Virus / worm | Needs a carrier and a user / spreads by itself |
| Signature / behaviour-based detection | Finds the known quickly / catches the new, can raise false alarms |
| OAuth 2.0 / OpenID Connect | Delegation / identity |
| Policy / standard | What and why / a measurable rule |
| Compliance / security | The boxes are ticked / the controls work every day |

## Where next

This module built the concepts. The next modules of the track build on
them: **Cryptography** opens up hashing, encryption and signatures;
**Network and Web Security** covers how requests are protected on the
network and the common vulnerabilities of web applications; **System
Security and Operations** covers hardening systems, monitoring logs and
incident response.

## Summary

- Security is protecting an asset against particular threats, according to
  risk; CIA says what was broken, risk says how much it matters.
- Decisions rest on principles: least privilege, deny by default, defence
  in depth, separation of duties.
- The path of a request: authentication → authorization → log.
- People, malware and accounts are part of the attack surface too.
- It is all managed with written policies and standards; but what is
  measured is not the boxes but whether the controls actually work.
