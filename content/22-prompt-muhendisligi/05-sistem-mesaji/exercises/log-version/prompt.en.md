`log_entry(system, reply)` should return a log dictionary:
`"system_version"`: the first 8 characters of the SHA-256 digest
(`hexdigest()`) of the system message's UTF-8 bytes; `"reply_words"`: the
number of words in the answer (`reply.split()`).

**Expected output:**

```
213c22ed 4
False
```
