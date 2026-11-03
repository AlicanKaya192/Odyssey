`string_to_mode(text)` should turn a nine-letter permission string
(`"rwxr-x---"`) into a number: `0o750`, that is `488`. Each letter is a
bit; if the letter is not `-` that bit is on. The string's first letter is
the highest bit (`0o400`), its last letter the lowest (`0o001`).

**Expected output:**

```
rwxr-xr-x 0o755
rw-r----- 0o640
rw------- 0o600
--------- 0o0
```
