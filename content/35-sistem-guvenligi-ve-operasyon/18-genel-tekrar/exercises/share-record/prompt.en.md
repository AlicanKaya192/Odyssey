`share_record(record, allowed, key)` should prepare a record to share
with another team: only the `allowed` fields stay, and if `email` stayed,
it is normalised with `strip().lower()` and turned into a pseudonym with
the first 12 characters of the `hmac.new(key.encode(), ...,
hashlib.sha256)` digest. The starter code uses a plain hash with no key.
Privacy and Data Protection, Secrets Management.

**Expected output:**

```
email 5e979343af4e
plan pro
```
