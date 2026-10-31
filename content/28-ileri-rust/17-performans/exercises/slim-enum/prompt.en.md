`Message` is over 257 bytes. Put the `Blob` variant in a `Box`, and fix `blob()` to match. `payload` stays the same, and the size must be at most 24.
