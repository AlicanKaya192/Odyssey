# Certificates and PKI

The Digital Signatures section left a question open: how do we know that
the public key we use to verify a signature **really** belongs to that
person or site? The "someone in the middle" problem from the Diffie-Hellman
section leads to the same place. The answer is the **certificate**: a
document, signed by a trusted authority, that binds a public key to an
identity. The whole of these authorities and rules is called **public key
infrastructure** (**PKI**).

## What a certificate binds

The most important fields of a certificate:

| Field | Example | Meaning |
|---|---|---|
| `subject` | `shop.example.test` | The key's owner |
| `e`, `n` | the public key | The owner's public key |
| `issuer` | `Toy Root CA` | The signing authority |
| `not_before`, `not_after` | `2026-01-01`, `2026-12-31` | The validity period |
| `signature` | a number | The authority's signature over the other fields |

When the authority (certificate authority, **CA**) signs the certificate,
it says "this public key belongs to this name". Let us build a toy
certificate; what gets signed is the sorted JSON of every field except
`signature`.

```python
import hashlib
import json


def digest(data, n):
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big") % n


def tbs(cert):
    body = {k: v for k, v in cert.items() if k != "signature"}
    return json.dumps(body, sort_keys=True).encode()


def issue(fields, issuer_name, issuer_d, issuer_n):
    cert = dict(fields, issuer=issuer_name)
    cert["signature"] = pow(digest(tbs(cert), issuer_n), issuer_d, issuer_n)
    return cert


def check_signature(cert, issuer_e, issuer_n):
    return pow(cert["signature"], issuer_e, issuer_n) == digest(tbs(cert), issuer_n)


ca_n = 104723 * 104729
ca_d = pow(65537, -1, (104723 - 1) * (104729 - 1))
site_n = 104717 * 104743
leaf = issue({"subject": "shop.example.test", "e": 65537, "n": site_n,
              "not_before": "2026-01-01", "not_after": "2026-12-31"},
             "Toy Root CA", ca_d, ca_n)
print(leaf["issuer"], "->", leaf["subject"])
print(check_signature(leaf, 65537, ca_n))
```

```text
Toy Root CA -> shop.example.test
True
```

Anyone who knows the CA's public key could verify that the certificate is
genuine. `tbs` (to be signed) produces the bytes to sign **in the same
order every time**: without `sort_keys=True`, the same certificate could
give two different byte strings.

## A changed certificate

Changing the public key or the name inside the certificate breaks the
signature:

```python
fake_key = dict(leaf, n=12345)
fake_name = dict(leaf, subject="bank.example.test")
print(check_signature(fake_key, 65537, ca_n))
print(check_signature(fake_name, 65537, ca_n))
```

```text
False
False
```

That is why a certificate can be sent in the clear: someone who changes the
information inside cannot make a valid signature without the CA's private
key.

## The chain of trust

Browsers and operating systems carry a few hundred **root certificates** in
advance, in a **trust store**. Root CAs usually do not sign certificates
directly; they sign an **intermediate CA**, and the intermediate CA signs
the sites' certificates. Verification asks at every link from the site to
the root "did the one above sign this certificate?", and at the end checks
whether the root is in the trust store.

```python
mid_n = 104701 * 104707
mid_d = pow(65537, -1, (104701 - 1) * (104707 - 1))
root = issue({"subject": "Toy Root CA", "e": 65537, "n": ca_n},
             "Toy Root CA", ca_d, ca_n)
mid = issue({"subject": "Toy Issuing CA", "e": 65537, "n": mid_n},
            "Toy Root CA", ca_d, ca_n)
site = issue({"subject": "shop.example.test", "e": 65537, "n": site_n},
             "Toy Issuing CA", mid_d, mid_n)


def verify_chain(chain, trusted):
    for cert, parent in zip(chain, chain[1:]):
        if cert["issuer"] != parent["subject"]:
            return "issuer mismatch"
        if not check_signature(cert, parent["e"], parent["n"]):
            return "bad signature"
    top = chain[-1]
    if trusted.get(top["subject"]) != [top["e"], top["n"]]:
        return "untrusted root"
    return "ok"


trusted = {"Toy Root CA": [65537, ca_n]}
print(verify_chain([site, mid, root], trusted))
print(verify_chain([site, mid, root], {}))
print(verify_chain([site, root], trusted))
```

```text
ok
untrusted root
issuer mismatch
```

With the full chain, verification passed. If the trust store is empty, the
chain is **untrusted** even though it is consistent in itself: anyone can
set up their own root and issue themselves a certificate; what matters is
that the root is on the list trusted in advance. With the intermediate
certificate missing, the signer of the site certificate could not be found.

## A signature is not enough: date and name

A certificate with a correct signature can still be rejected. The verifier
checks two more things: **is today inside the validity period**, and **does
the name in the certificate match the name being connected to**. The name
can be a **wildcard** (`*.example.test`); a wildcard stands for **only one**
label.

```python
def in_date(cert, today):
    return cert["not_before"] <= today <= cert["not_after"]


def host_matches(pattern, host):
    if pattern.startswith("*."):
        suffix = pattern[1:]
        rest = host[: -len(suffix)]
        return host.endswith(suffix) and rest != "" and "." not in rest
    return pattern == host


print(in_date(leaf, "2026-11-03"), in_date(leaf, "2027-01-15"))
print(host_matches("shop.example.test", "shop.example.test"))
print(host_matches("*.example.test", "shop.example.test"))
print(host_matches("*.example.test", "a.b.example.test"))
print(host_matches("shop.example.test", "shop.example.test.evil.test"))
```

```text
True False
True
True
False
False
```

Since the dates are in `YYYY-MM-DD` form, comparing them as text gives the
right order. The wildcard did not cover `a.b.example.test`, and the name did
not match when embedded in another domain. Real verifiers take the name
from the certificate's **Subject Alternative Name** (SAN) list rather than
`subject`.

## Revocation and transparency

- **Revocation:** if a private key is stolen, the certificate is revoked
  before it expires. Revocation lists (CRL) or an online query (OCSP)
  announce this. Because revocation information cannot always be reached,
  certificate lifetimes are kept short today (measured in months).
- **Certificate Transparency:** CAs write every certificate they issue into
  public, append-only logs. A domain's owner can see there a certificate
  issued in their name without their knowledge.
- **Automatic renewal:** the ACME protocol automates getting and renewing
  certificates; that way short-lived certificates are no burden.

## Summary

- A **certificate** binds a public key to a name; a **CA** signs it.
- If any field of the certificate changes, the signature does not match.
- **Chain of trust:** site → intermediate CA → root; the root must already
  be in the **trust store**.
- A signature is not enough: the **validity dates** and the **name match**
  are checked too; a wildcard covers one label.
- **Revocation** (CRL, OCSP), **transparency logs** and short-lived,
  automatically renewed certificates keep the system working.
