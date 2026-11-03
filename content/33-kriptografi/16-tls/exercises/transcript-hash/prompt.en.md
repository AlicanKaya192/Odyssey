`transcript_hash(messages)` should add the messages **in the order they
arrived** to one SHA-256 (`m.encode()`) and return the hex hash. The
starter code sorts the messages; then a handshake with its order changed
gives the same hash.

**Expected output:**

```
False
64
```
