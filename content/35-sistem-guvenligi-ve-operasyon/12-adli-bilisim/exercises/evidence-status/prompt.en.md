`evidence` is evidence name → content (text), `recorded` is name → the
SHA-256 recorded at collection (`hashlib.sha256(content.encode()).hexdigest()`).
`evidence_status(evidence, recorded)` should return one line per piece of
evidence, alphabetical by name: `"<name>: intact"` if the hash matches,
`"<name>: altered"` if not, `"<name>: unrecorded"` if there is no record.

**Expected output:**

```
image-1: intact
image-2: altered
image-3: unrecorded
```
