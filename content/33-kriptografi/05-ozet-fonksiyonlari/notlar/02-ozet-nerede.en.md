Hash functions are the unseen part of many systems you use every day.
Knowing where each one is used makes it easier to see which property is at
work.

## Integrity: "has this file changed?"

A SHA-256 value is published next to a downloaded installer. The person who
downloads the file computes the digest on their own computer and compares;
if it does not match, the file was corrupted or changed on the way. The
property used: **deterministic** and the **avalanche effect**.

## Fingerprint: "are these two the same?"

Instead of comparing large files, their digests are compared. Backup and
cloud storage use digests to avoid storing the same file twice
(deduplication). Version control systems (Git) name every file and every
commit by its digest. The property used: **collision resistant**.

## Commitment: "I decided in advance but will reveal it later"

When a value must be kept secret now and revealed later, the digest of the
value is published first. When the value is later revealed, everyone
computes its digest and sees that it matches the published one; the
publisher cannot slip in a change. The property used: **one-way** and
**collision resistant**.

## Building block: inside other tools

- **HMAC** (the next section) wraps a hash function with a key.
- **Password hashes** (Storing Passwords) slow the hash down and salt it.
- A **digital signature** (the Digital Signatures section) first takes the
  message's digest and then signs that: the signature works on the
  fixed-length digest, not the whole long message.

## Where is it not used?

- **In place of encryption:** a hash cannot be reversed; you cannot hash
  data you need to keep secret and read back later.
- **Plain password storage:** being fast hurts here; a slow salted hash is
  needed.
- **Keyless proof of integrity:** an attacker changes the data and the
  digest together; keyed HMAC is needed.
