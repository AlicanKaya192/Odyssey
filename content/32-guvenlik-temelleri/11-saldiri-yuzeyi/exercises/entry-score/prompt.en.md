The toy score from the lesson: the weight from the `WEIGHT` dictionary
(internet 3, internal 2, local 1), doubled if there is no authentication.

`entry_score(exposure, auth)` should compute it. If an exposure that is not
in the dictionary comes in (for example `"partner"`), count it as the
**most exposed** level, like the internet (3): do not assume a path you do
not know is safe.

**Expected output:**

```
3
6
2
3
```
