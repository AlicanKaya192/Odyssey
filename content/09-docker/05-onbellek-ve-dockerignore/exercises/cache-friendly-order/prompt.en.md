This Dockerfile works, but `pip install` runs from scratch on every code
change.

**What to do:** make the order cache-friendly: first copy only
`requirements.txt`, install the packages, **then** copy all of the code.

After running, you cannot change `app.py` (it is read-only), but look at the
steps in the terminal: on the second run they are all `CACHED`.

**Expected output:**

```
built with a warm cache
```
