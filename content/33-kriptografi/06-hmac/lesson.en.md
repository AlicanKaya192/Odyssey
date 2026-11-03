# Message Authentication: HMAC

The Hash Functions section ended with a warning: a plain hash protects data
against **accidental** corruption but not against a **deliberate** change.
The attacker changes the data and recomputes the hash. In the XOR and the
One-Time Pad section we also saw that encryption does not give integrity,
that the ciphertext can be changed bit by bit. This section covers the tool
that answers two questions at once: **has the message changed** and **was
it sent by someone who knows the key**.

## A message authentication code (MAC)

The fix is to mix a **secret key** into the hash. The sender and the
receiver share the same key. The sender adds a **tag** computed with the
key next to the message; the receiver recomputes the tag with the same key
and compares. Someone who does not know the key cannot produce a valid tag.
This tag is called a **message authentication code** (MAC).

The most common MAC is **HMAC**, which wraps a hash function with a key. It
comes ready in Python's standard library:

```python
import hashlib
import hmac

key = b"shared-secret-key"
message = b"transfer 100 to bob"
tag = hmac.new(key, message, hashlib.sha256).hexdigest()
print(tag[:32])
print(len(tag))
```

```text
c3e2b5cb52e9b0f62c7efef90eb5b2c7
64
```

The tag is a fingerprint of the message and the key together; being based
on SHA-256 it is 64 hex digits. This is exactly how we signed the toy token
in the Identity Management and Single Sign-On section.

## Verification

The receiver takes the message and the tag and recomputes the tag with
their own key. If the message or the tag has changed, the new tag does not
match:

```python
import hashlib
import hmac


def verify(key, message, tag):
    expected = hmac.new(key, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, tag)


key = b"shared-secret-key"
message = b"transfer 100 to bob"
tag = hmac.new(key, message, hashlib.sha256).hexdigest()

print(verify(key, message, tag))
print(verify(key, b"transfer 900 to eve", tag))
print(verify(b"wrong-key", message, tag))
```

```text
True
False
False
```

- The first line is `True`: the message and tag did not change.
- The second line is `False`: the message changed, and the attacker could
  not produce a tag for the new message because they do not know the key.
  The `PAY BOB 100` → `PAY BOB 900` attack from the XOR section is now
  caught.
- The third line is `False`: the key is wrong.

## Why not `sha256(key + message)`?

The first idea that comes to mind is "put the key in front of the message
and hash it". But the internal structure of common hash functions leaves
this open to a vulnerability called a **length-extension** attack: without
knowing the key, the attacker can append to the **end** of a message that
has a valid tag and produce a valid tag for the new message too. We do not
go into the details; what matters is that HMAC is built with a special
construction that does not have this problem (mixing the key in twice, with
different paddings). **Do not write `sha256(key + message)` yourself; use
the `hmac` module.** It is a small but typical example of the "don't write
your own crypto" rule from the Security Principles section.

## Why not compare with `==`?

Writing `expected == tag` while verifying gives the right result but opens a
side channel. Python's `==` operator **stops at the first differing byte**
when comparing two strings; a guess close to the right tag takes slightly
longer than a far one. An attacker who measures this time difference can
find the tag byte by byte. `hmac.compare_digest` compares in the **same
time** wherever the difference is (constant-time comparison):

```python
import hmac

a = "a" * 64
b = "a" * 63 + "b"
print(a == a, hmac.compare_digest(a, a))
print(a == b, hmac.compare_digest(a, b))
```

```text
True True
False False
```

The results are the same (`True`/`False`), but `compare_digest` does not
give away the timing. It is used everywhere a tag, a password hash or a
token is compared. We also compared password hashes with it in the Storing
Passwords section.

## MAC or signature?

<figure class="fig"><div class="versus">
  <div><h4>HMAC (symmetric)</h4>The sender and receiver share the <b>same</b> secret key. It is fast. But because either side can produce the tag, one side cannot <b>prove to a third party</b> that "the other sent this".</div>
  <div><h4>Digital signature (asymmetric)</h4>The sender signs with their <b>private</b> key, anyone verifies with the <b>public</b> key. It is slow. Because only the owner of the private key can produce it, it gives proof to a third party (<b>non-repudiation</b>).</div>
</div><figcaption>HMAC for integrity between two sides; a signature for proof to a third party (the Digital Signatures section).</figcaption></figure>

Remember the table in the What Is Security? The CIA Triad section: HMAC
provides integrity and authenticity; non-repudiation needs a digital
signature.

## Verify first, then use

When handling an authenticated message the order matters: **check the tag
first, and if it does not match do not open the message at all.** We saw
the same rule for the token in the Identity Management section: signature
first, then content.

```python
import hashlib
import hmac

KEY = b"shared-secret-key"


def handle(message, tag):
    expected = hmac.new(KEY, message, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, tag):
        return "rejected"
    return "accepted: " + message.decode()


msg = b"ok"
good = hmac.new(KEY, msg, hashlib.sha256).hexdigest()
print(handle(msg, good))
print(handle(b"tampered", good))
```

```text
accepted: ok
rejected
```

The message whose tag did not match was rejected without being opened. This
lays the ground for the Authenticated Encryption section: there, encryption
and a MAC work together to give both confidentiality and integrity.

## Summary

- A **MAC** proves the message has not changed **and** came from someone
  who knows the key; this is what a plain hash cannot do.
- **HMAC** wraps a hash function with a key; `hmac.new(key, message,
  hashlib.sha256)`.
- **Do not write `sha256(key + message)`:** it is open to length extension.
  Use the `hmac` module.
- Compare tags with **`hmac.compare_digest`**: constant-time, does not give
  away timing.
- **HMAC is symmetric** (a shared key, no non-repudiation); proof to a
  third party needs a **digital signature**.
- With an authenticated message, **check the tag first, then use the
  content.**
