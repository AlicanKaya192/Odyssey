Write the function that works out which reduce machine a key goes to, in a
way that gives the same answer in every process.

**What to do:**

Write the function `partition(key, reducers)`:

- Turn the key into bytes: `key.encode()`.
- Take its stable hash: `zlib.crc32(...)`.
- Return the remainder of dividing by the number of machines: `% reducers`.

Do not use Python's `hash()`: a string's hash differs in every process.

Example: `partition("Istanbul", 4)` → `1`.
