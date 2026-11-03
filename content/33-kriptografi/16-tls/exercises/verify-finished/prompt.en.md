`transcript_hash` is ready. `verify_finished(key_hex, messages, tag_hex)`
should verify the incoming Finished tag: HMAC-SHA256, key `key_hex`, the
data is the transcript hash of **all** messages; compare with
`hmac.compare_digest`. The starter code hashes only the last message; a
change in the first message goes unnoticed.

**Expected output:**

```
True
False
```
